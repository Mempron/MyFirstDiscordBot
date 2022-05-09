import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from vkbottle import VKAPIError

import typing
from random import randint

from config import config, database, api


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description=config.text['ping_description'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    @app_commands.describe(target=config.text['ping_describe_target'],
                           note=config.text['ping_describe_note'])
    async def ping(self, interaction: discord.Interaction, target: typing.Union[discord.Role, discord.Member],
                   note: str = None):

        await interaction.response.defer()

        targets = []
        vacationers = []

        if isinstance(target, discord.role.Role):
            for member in target.members:
                vacation = get(member.roles, id=config.discord_bot.vac_role)
                if vacation:
                    vacationers.append(member)
            targets = list(set(target.members) - set(vacationers))
        elif isinstance(target, discord.Member):
            vacation = get(target.roles, id=config.discord_bot.vac_role)
            if vacation:
                vacationers.append(target)
            else:
                targets.append(target)

        if vacationers:
            ds_users_names = ', '.join([vacationer.name for vacationer in vacationers])

            embed = discord.Embed(
                title=config.text['vacation_error_embed_title'],
                description=config.text['vacation_error_embed_description'].format(ds_users_names=ds_users_names),
                colour=discord.Colour.red()
            )
            embed.set_image(url=config.text['vacation_error_embed_image'])

            await interaction.followup.send(embed=embed)

        if targets:
            ds_ids_vk_ids_with_vk_error_901 = []
            channel_name = interaction.channel.name

            try:
                if interaction.channel.parent:
                    channel_name = interaction.channel.parent.name + ' \u2192 ' + channel_name
            except AttributeError:
                pass

            cursor = database.cursor()
            ds_users_ids = ", ".join([str(target.id) for target in targets])
            cursor.execute(f'SELECT * FROM "Users" WHERE ds_id IN ({ds_users_ids});')
            ds_ids_vk_ids = cursor.fetchall()

            for ds_id_vk_id in ds_ids_vk_ids:

                vk_user = await api.users.get(user_ids=[ds_id_vk_id[1]])
                vk_user = vk_user[0]

                try:

                    if note:
                        await api.messages.send(peer_id=vk_user.id,
                                                random_id=randint(0, 500000),
                                                message=config.text['ping_vk_direct_message'].format(
                                                    vk_user_name=vk_user.first_name,
                                                    channel=channel_name,
                                                    note=f'\nЗаметка:\n{note}'
                                                ))
                    else:
                        await api.messages.send(peer_id=vk_user.id,
                                                random_id=randint(0, 500000),
                                                message=config.text['ping_vk_direct_message'].format(
                                                    vk_user_name=vk_user.first_name,
                                                    channel=channel_name,
                                                    note=''
                                                ))

                except VKAPIError[901]:
                    ds_ids_vk_ids_with_vk_error_901.append(ds_id_vk_id)

            if ds_ids_vk_ids_with_vk_error_901:
                linked_accounts_names = ''
                ds_users = []

                all_ds_users = self.bot.get_all_members()
                for ds_id_vk_id in ds_ids_vk_ids_with_vk_error_901:
                    ds_user = get(all_ds_users, id=ds_id_vk_id[0])
                    vk_user = await api.users.get(user_ids=[ds_id_vk_id[1]], name_case='gen')
                    vk_user = vk_user[0]

                    linked_accounts_names += '\nАккаунт ' + ds_user.name + 'связан с аккаунтом ' + vk_user.first_name \
                                             + ' ' + vk_user.last_name
                    ds_users.append(ds_user)

                embed = discord.Embed(
                    title=config.text['ping_embed_error_VKAPIError_901_title'],
                    description=config.text['ping_embed_error_VKAPIError_901_description'].format(
                        linked_accounts_names=linked_accounts_names),
                    colour=discord.Colour.red()
                )
                embed.set_image(url=config.text['ping_embed_error_VKAPIError_901_image'])
                mentions = ', '.join(ds_user.mention for ds_user in ds_users)
                await interaction.followup.send(embed=embed,
                                                content=mentions)

            if note:
                await api.messages.send(peer_id=2000000002,
                                        random_id=randint(0, 100000),
                                        message=config.text['ping_vk_group_chat_message'].format(
                                            ds_users_names=', '.join([target.name for target in targets]),
                                            channel=channel_name,
                                            note=f'\nЗаметка:\n{note}'
                                        ))
            else:
                await api.messages.send(peer_id=2000000002,
                                        random_id=randint(0, 100000),
                                        message=config.text['ping_vk_group_chat_message'].format(
                                            ds_users_names=', '.join([target.name for target in targets]),
                                            channel=channel_name,
                                            note=''
                                        ))

            if not ds_ids_vk_ids_with_vk_error_901:
                embed = discord.Embed(
                    title=config.text['ping_embed_title'],
                    description=config.text['ping_embed_description'].format(
                        ds_users_names=', '.join([target.mention for target in targets])),
                    colour=discord.Colour.blue()
                )
                embed.set_image(url=config.text['ping_embed_image'])
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=config.text['ping_embed_error_not_full_title'],
                    description=config.text['ping_embed_error_not_full_description'].format(ds_users_names=', '.join(
                        [target.name for target in targets])),
                    colour=discord.Colour.orange()
                )
                embed.set_image(url=config.text['ping_embed_error_not_full_image'])
                await interaction.followup.send(embed=embed)

    @ping.error
    async def ping_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.MissingAnyRole):
            embed = discord.Embed(
                title=config.text['embed_error_missing_any_role_title'],
                description=config.text['embed_error_missing_any_role_description'].format(
                    ds_user_name=interaction.user.name),
                colour=discord.Colour.red()
            )
            embed.set_image(url=config.text['embed_error_missing_any_role_image'])
            await interaction.followup.send(embed=embed)
            return

        error_text = f'{type(error)}\n{error}'
        if error.original:
            error_text += f'\n{type(error.original)}\n{error.original}'

        embed = discord.Embed(
            title=config.text['unknown_error_embed_title'],
            description=config.text['unknown_error_embed_description'].format(error=error_text),
            colour=discord.Colour.red()
        )
        embed.set_image(url=config.text['unknown_error_embed_image'])
        await interaction.followup.send(embed=embed)

        print('Хьюстон, у нас проблема!')
        print(f'{interaction.user.name} натворил делов!')

        print('---------------------')
        print(f'Type of Error: {type(error)}')
        print(f'Error: {error}')
        if error.original:
            print('---------------------')
            print('Which contains another error:')
            print(f'Type of Error: {type(error.original)}')
            print(f'Error: {error.original}')


async def setup(bot):
    await bot.add_cog(PingCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
