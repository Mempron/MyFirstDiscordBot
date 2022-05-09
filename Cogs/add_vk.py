import discord
from discord import app_commands
from discord.ext import commands
from psycopg2.errors import UniqueViolation
from vkbottle import VKAPIError

from random import randint

from config import config, database, api


class AddVKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='add_vk', description=config.text['add_vk_description'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    @app_commands.describe(ds_user=config.text['add_vk_describe_ds_user'],
                           vk_id=config.text['add_vk_describe_vk_id'])
    async def add_vk(self, interaction: discord.Interaction, ds_user: discord.Member, vk_id: str):
        vk_user = await api.users.get(user_ids=vk_id, fields=['photo_400_orig'],
                                      name_case=config.text['vk_users_get_name_case'])
        vk_user = vk_user[0]

        cursor = database.cursor()
        cursor.execute(f'SELECT * FROM "Users" WHERE ds_id = {ds_user.id} OR vk_id = {vk_user.id}')
        id_exist = cursor.fetchone()

        if id_exist:
            raise UniqueViolation

        cursor.execute(f'INSERT INTO "Users" (ds_id, vk_id) VALUES ({ds_user.id}, {vk_user.id})')
        database.commit()

        try:
            await api.messages.send(peer_id=vk_user.id, random_id=randint(0, 500000),
                                    message=f'Теперь ваш профиль ВК связан с Discord профилем с именем: '
                                            f'{ds_user.name}.\nВаши профили связал(а): {interaction.user.name}')
        except VKAPIError[901]:
            embed = discord.Embed(
                title=config.text['add_vk_embed_error_VKAPIError_901_title'],
                description=config.text['add_vk_embed_error_VKAPIError_901_description'].format(
                    vk_user_name=f'[{vk_user.first_name} {vk_user.last_name}](https://vk.com/id{vk_user.id})',
                    ds_user_name=ds_user.mention),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=config.text['add_vk_embed_error_VKAPIError_901_image'])
            await interaction.response.send_message(embed=embed, content=ds_user.mention)
            return

        embed = discord.Embed(
            title=config.text['add_vk_embed_title'],
            description=config.text['add_vk_embed_description'].format(
                vk_user_name=f'[{vk_user.first_name} {vk_user.last_name}](https://vk.com/id{vk_user.id})',
                ds_user_name=ds_user.mention),
            colour=discord.Colour.blue()
        )
        embed.set_image(url=config.text['add_vk_embed_image'])
        await interaction.response.send_message(embed=embed, content=ds_user.mention)

    @add_vk.error
    async def add_vk_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandInvokeError):
            if isinstance(error.original, UniqueViolation):
                embed = discord.Embed(
                    title=config.text['add_vk_embed_error_unique_violation_title'],
                    description=config.text['add_vk_embed_error_unique_violation_description'],
                    colour=discord.Colour.red()
                )
                embed.set_image(url=config.text['add_vk_embed_error_unique_violation_image'])
                await interaction.response.send_message(embed=embed)
                return

            elif isinstance(error.original, IndexError):
                embed = discord.Embed(
                    title=config.text['add_vk_embed_error_index_error_title'].format(
                        vk_id=interaction.namespace.vk_id),
                    description=config.text['add_vk_embed_error_index_error_description'],
                    colour=discord.Colour.red()
                )
                embed.set_image(url=config.text['add_vk_embed_error_index_error_image'])
                await interaction.response.send_message(embed=embed)
                return

        elif isinstance(error, discord.app_commands.errors.MissingAnyRole):
            embed = discord.Embed(
                title=config.text['embed_error_missing_any_role_title'],
                description=config.text['embed_error_missing_any_role_description'].format(
                    ds_user_name=interaction.user.name),
                colour=discord.Colour.red()
            )
            embed.set_image(url=config.text['embed_error_missing_any_role_image'])
            await interaction.response.send_message(embed=embed)
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
        await interaction.response.send_message(embed=embed)

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
    await bot.add_cog(AddVKCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
