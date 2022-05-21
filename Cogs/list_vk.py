import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import vkbottle
import psycopg2

from config import config
from text import text


class ListVKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='list_vk', description=text['list_vk_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    async def list_vk(self, interaction: discord.Interaction):
        await interaction.response.defer()

        data_base_connection = psycopg2.connect(
            host=config.db.host,
            port=config.db.port,
            database=config.db.name,
            user=config.db.user,
            password=config.db.password
        )
        data_base_cursor = data_base_connection.cursor()

        data_base_cursor.execute('SELECT ds_id, vk_id FROM "Users"')
        users = data_base_cursor.fetchall()
        data_base_cursor.close()
        data_base_connection.close()

        if users:
            vk = vkbottle.API(config.vbot.token)

            guild = self.bot.get_guild(config.dbot.privileged_guild)
            members = guild.members

            links = ''

            for ds_id, vk_id in users:
                ds_user = get(members, id=ds_id)
                vk_user = await vk.users.get(user_ids=vk_id, name_case='ins')
                vk_user = vk_user[0]

                links += f'\nАккаунт {ds_user.mention} связан с ' \
                         f'[{vk_user.first_name} {vk_user.last_name}](https://vk.com/id{vk_user.id}).'

            embed = discord.Embed(
                title=text['list_vk_embed_title'],
                description=text['list_vk_embed_description'].format(links=links),
                colour=discord.Colour.blue()
            )
            embed.set_image(url=text['list_vk_embed_image'])
            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                title=text['list_vk_embed_error_nothing_in_list_title'],
                description=text['list_vk_embed_error_nothing_in_list_description'],
                colour=discord.Colour.orange()
            )
            embed.set_image(url=text['list_vk_embed_error_nothing_in_list_image'])
            await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ListVKCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
