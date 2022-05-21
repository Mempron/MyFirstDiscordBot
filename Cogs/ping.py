import discord
from discord import app_commands
from discord.ext import commands
import psycopg2
import vkbottle
from vkbottle import VKAPIError

import typing
from random import randint
from dataclasses import dataclass

from config import config
from text import text
from Utils.get_targets import get_targets


@dataclass
class User:
    ds_id: int
    vk_id: int


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Подтвердить', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(label='Отменить', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description=text['ping_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    @app_commands.describe(
        target=text['ping_describe_target'],
        note=text['ping_describe_note']
    )
    @app_commands.choices(choice=[
        app_commands.Choice(name='в беседу и в лс', value=0),
        app_commands.Choice(name='только в беседу', value=1),
        app_commands.Choice(name='только в лс', value=2)
    ])
    async def ping(
            self,
            interaction: discord.Interaction,
            target: typing.Union[discord.Role, discord.Member],
            choice: app_commands.Choice[int],
            note: str = None
    ):
        await interaction.response.defer()

        targets = await get_targets(interaction, target)

        if targets:
            data_base_connection = psycopg2.connect(
                host=config.db.host,
                port=config.db.port,
                database=config.db.name,
                user=config.db.user,
                password=config.db.password
            )
            data_base_cursor = data_base_connection.cursor()

            data_base_cursor.execute(
                f'SELECT ds_id, vk_id '
                f'FROM "Users" '
                f'WHERE ds_id IN ({", ".join(str(target.id) for target in targets)}); ')
            users = [User(*user) for user in data_base_cursor.fetchall()]

            data_base_cursor.close()
            data_base_connection.close()

            vk = vkbottle.API(config.vbot.token)
            vk_users = await vk.users.get(user_ids=[user.vk_id for user in users])

            users.sort(key=lambda user: user.vk_id)
            vk_users.sort(key=lambda vk_user: vk_user.id)

            targets = [[target, None] for target in targets]

            for target in targets:
                for i in range(len(users)):
                    if target[0].id == users[i].ds_id:
                        target[1] = vk_users[i]
                        break
                target = (target[0], target[1])

            where = ''
            if choice.value == 0:
                where = 'в беседу и в личные сообщения'
            elif choice.value == 1:
                where = 'в беседу'
            elif choice.value == 2:
                where = 'в личные сообщения'

            list_users = ''
            for target in targets:
                list_users += f'\n\u2022 {target[0].mention}'
                if target[1]:
                    list_users += f' \u2192 ' \
                                  f'[{target[1].first_name} {target[1].last_name}](https://vk.com/id{target[1].id})'

            embed = discord.Embed(
                title=text['ping_embed_confirm_form_title'],
                description=text['ping_embed_confirm_form_description'].format(
                    total=str(len(targets)),
                    where=where,
                    list_users=list_users
                ),
                colour=discord.Colour.dark_gold()
            )
            embed.set_image(url=text['ping_embed_confirm_form_image'])
            view = Confirm()

            if len(targets) > 1:
                message = await interaction.followup.send(embed=embed, view=view)
                await view.wait()
                await message.delete()
            else:
                view.value = True

            if view.value:
                channel_name = interaction.channel.name
                try:
                    if interaction.channel.parent:
                        channel_name = interaction.channel.parent.name + ' \u2192 ' + channel_name
                except AttributeError:
                    pass

                if note:
                    note = f'\nЗаметка:\n{note}'
                else:
                    note = ''

                not_success_ping = []

                if choice.value == 0 or choice.value == 1:

                    list_users_to_ping = ''
                    for target in targets:
                        if target[1]:
                            list_users_to_ping += f'\n[id{target[1].id}|{target[0].name}]'
                        else:
                            list_users_to_ping += f'\n{target[0].name}'
                            if target not in not_success_ping:
                                not_success_ping.append(target)

                    await vk.messages.send(
                        peer_id=2000000003,
                        random_id=randint(0, 100000),
                        message=text['ping_vk_group_chat_message'].format(
                            ds_users_names=list_users_to_ping,
                            channel=channel_name,
                            note=note
                        )
                    )

                if choice.value == 0 or choice.value == 2:
                    for target in targets:
                        if target[1]:
                            try:
                                await vk.messages.send(
                                    peer_id=target[1].id,
                                    random_id=randint(0, 100000),
                                    message=text['ping_vk_direct_message'].format(
                                        vk_user_name=target[1].first_name,
                                        channel=channel_name,
                                        note=note
                                    )
                                )
                            except VKAPIError[901]:
                                if target not in not_success_ping:
                                    not_success_ping.append(target)
                        else:
                            if target not in not_success_ping:
                                not_success_ping.append(target)

                success_ping = []
                if len(targets) > len(not_success_ping):
                    check = [user[0].id for user in not_success_ping]
                    for target in targets:
                        if target[0].id not in check:
                            success_ping.append(target)

                if not_success_ping:
                    linked_accounts_names = ''

                    for target in not_success_ping:
                        linked_accounts_names += f'\n\u2022 {target[0].mention}'
                        if target[1]:
                            linked_accounts_names += f' \u2192 [{target[1].first_name} {target[1].last_name}]' \
                                                     f'(https://vk.com/id{target[1].id})'

                    embed = discord.Embed(
                        title=text['ping_embed_error_VKAPIError_901_title'],
                        description=text['ping_embed_error_VKAPIError_901_description'].format(
                            linked_accounts_names=linked_accounts_names
                        ),
                        colour=discord.Colour.brand_red()
                    )
                    embed.set_image(url=text['ping_embed_error_VKAPIError_901_image'])

                    await interaction.followup.send(embed=embed)

                    format_text = ''
                    for user in not_success_ping:
                        if user[1]:
                            format_text += f'\n[id{user[1].id}|{user[0].name}]'
                        else:
                            format_text += f'\n{user[0].name}'

                    await vk.messages.send(
                        peer_id=2000000005,
                        random_id=randint(0, 100000),
                        message=f'Не смог пингануть или упомянуть {where} следующих:'
                                f'{format_text}\n'
                                f'Откуда: {channel_name}\n'
                                f'{note}'
                    )
                    if len(not_success_ping) == 1:
                        return

                if success_ping:
                    format_list = ''
                    for target in success_ping:
                        format_list += f'\n\u2022 {target[0].mention} \u2192 [{target[1].first_name} ' \
                                       f'{target[1].last_name}]' \
                                       f'(https://vk.com/id{target[1].id})'

                    embed = discord.Embed(
                        title=text['ping_embed_error_not_full_title'],
                        description=text['ping_embed_error_not_full_description'].format(
                            ds_users_names=format_list
                        ),
                        colour=discord.Colour.dark_magenta()
                    )
                    embed.set_image(url=text['ping_embed_error_not_full_image'])
                    await interaction.followup.send(embed=embed)

                    format_text = ''
                    for user in success_ping:
                        format_text += f'\n[id{user[1].id}|{user[0].name}]'
                    await vk.messages.send(
                        peer_id=2000000005,
                        random_id=randint(0, 100000),
                        message=f'Пинганул или упомянул {where} следующих:'
                                f'{format_text}\n'
                                f'Откуда: {channel_name}\n'
                                f'{note}'
                    )
        else:
            embed = discord.Embed(
                title=text['ping_embed_error_no_targets_title'],
                description=text['ping_embed_error_no_targets_description'],
                colour=discord.Colour.random()
            )
            embed.set_image(url=text['ping_embed_error_no_targets_image'])
            await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PingCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
