import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import psycopg2

import typing

from config import config
from text import text
from Utils.get_targets import get_targets


class CancelVacCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='cancel_vac', description=text['cancel_vac_description'])
    @app_commands.describe(target=text['cancel_vac_describe_target'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    async def cancel_vac(self, interaction: discord.Interaction, target: typing.Union[discord.Role, discord.Member]):

        await interaction.response.defer()

        targets, vacationers = await get_targets(interaction, target)

        if targets:
            ds_users_names = ', '.join([target.mention for target in targets])
            embed = discord.Embed(
                title=text['cancel_vac_embed_error_no_vac_title'],
                description=text['cancel_vac_embed_error_no_vac_description'].format(ds_users_names=ds_users_names),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=text['cancel_vac_embed_error_no_vac_image'])
            await interaction.followup.send(embed=embed)

        if vacationers:
            ds_users_names = ', '.join([vacationer.mention for vacationer in vacationers])
            embed = discord.Embed(
                title=text['cancel_vac_embed_title'],
                description=text['cancel_vac_embed_description'].format(ds_users_names=ds_users_names),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=text['cancel_vac_embed_image'])
            await interaction.followup.send(embed=embed, content=ds_users_names)

            data_base_connection = psycopg2.connect(
                host=config.db.host,
                port=config.db.port,
                database=config.db.name,
                user=config.db.user,
                password=config.db.password
            )
            data_base_cursor = data_base_connection.cursor()

            guild = self.bot.get_guild(config.dbot.privileged_guild)
            vac_role = get(guild.roles, id=config.dbot.vac_role)

            for vacationer in vacationers:
                await vacationer.remove_roles(vac_role)

                data_base_cursor.execute(f'DELETE FROM "Tasks" WHERE ds_id = {vacationer.id} '
                                         f'AND func_name = \'vac\' AND not complete_status')
                data_base_connection.commit()

            data_base_cursor.close()
            data_base_connection.close()


async def setup(bot):
    await bot.add_cog(CancelVacCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
