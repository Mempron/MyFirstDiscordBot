import discord

from discord import app_commands
from discord.ext import commands
import psycopg2
from psycopg2.errors import UniqueViolation
import vkbottle
from vkbottle import VKAPIError

from random import randint

from config import config
from text import text


class AddVKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='add_vk', description=text['add_vk_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    @app_commands.describe(
        ds_user=text['add_vk_describe_ds_user'],
        vk_id=text['add_vk_describe_vk_id']
    )
    async def add_vk(
            self,
            interaction: discord.Interaction,
            ds_user: discord.Member,
            vk_id: str
    ):
        await interaction.response.defer()

        vk = vkbottle.API(config.vbot.token)
        vk_user = await vk.users.get(
            user_ids=[vk_id],
            fields=['photo_400_orig'],
            name_case=text['add_vk_users_get_name_case']
        )
        vk_user = vk_user[0]

        data_base_connection = psycopg2.connect(
            host=config.db.host,
            port=config.db.port,
            database=config.db.name,
            user=config.db.user,
            password=config.db.password
        )
        data_base_cursor = data_base_connection.cursor()
        data_base_cursor.execute(f'SELECT * FROM "Users" WHERE ds_id = {ds_user.id} OR vk_id = {vk_user.id}')
        id_exist = data_base_cursor.fetchone()

        if id_exist:
            data_base_cursor.close()
            data_base_connection.close()
            raise UniqueViolation

        data_base_cursor.execute(f'INSERT INTO "Users" (ds_id, vk_id) VALUES ({ds_user.id}, {vk_user.id})')
        data_base_connection.commit()
        data_base_cursor.close()
        data_base_connection.close()

        try:
            await vk.messages.send(
                peer_id=vk_user.id,
                random_id=randint(0, 500000),
                message=f'Теперь ваш профиль ВК связан с Discord профилем с именем: '
                        f'{ds_user.name}.\nВаши профили связал(а): {interaction.user.name}'
            )

        except VKAPIError[901]:
            embed = discord.Embed(
                title=text['add_vk_embed_error_VKAPIError_901_title'],
                description=text['add_vk_embed_error_VKAPIError_901_description'].format(
                    vk_user_name=f'[{vk_user.first_name} {vk_user.last_name}](https://vk.com/id{vk_user.id})',
                    ds_user_name=ds_user.mention),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=text['add_vk_embed_error_VKAPIError_901_image'])
            await interaction.followup.send(embed=embed, content=ds_user.mention)
            return

        embed = discord.Embed(
            title=text['add_vk_embed_title'],
            description=text['add_vk_embed_description'].format(
                vk_user_name=f'[{vk_user.first_name} {vk_user.last_name}](https://vk.com/id{vk_user.id})',
                ds_user_name=ds_user.mention),
            colour=discord.Colour.blue()
        )
        embed.set_image(url=text['add_vk_embed_image'])
        await interaction.followup.send(embed=embed, content=ds_user.mention)

    @add_vk.error
    async def add_vk_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandInvokeError):
            if isinstance(error.original, UniqueViolation):
                interaction.extras['error_handled'] = True
                embed = discord.Embed(
                    title=text['add_vk_embed_error_unique_violation_title'],
                    description=text['add_vk_embed_error_unique_violation_description'],
                    colour=discord.Colour.red()
                )
                embed.set_image(url=text['add_vk_embed_error_unique_violation_image'])
                await interaction.followup.send(embed=embed)

            elif isinstance(error.original, IndexError):
                interaction.extras['error_handled'] = True
                embed = discord.Embed(
                    title=text['add_vk_embed_error_index_error_title'].format(
                        vk_id=interaction.namespace.vk_id),
                    description=text['add_vk_embed_error_index_error_description'],
                    colour=discord.Colour.red()
                )
                embed.set_image(url=text['add_vk_embed_error_index_error_image'])
                await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(AddVKCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
