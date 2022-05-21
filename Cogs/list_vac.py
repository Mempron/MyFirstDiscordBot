import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import psycopg2

import datetime
from dataclasses import dataclass

from config import config
from text import text


@dataclass
class Vac:
    member_id: discord.Member
    vacation_period: datetime.datetime
    note: str


class ListVacCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='list_vac', description=text['list_vac_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    async def list_vac(self, interaction: discord.Interaction):

        await interaction.response.defer()

        data_base_connection = psycopg2.connect(
            host=config.db.host,
            port=config.db.port,
            database=config.db.name,
            user=config.db.user,
            password=config.db.password
        )
        data_base_cursor = data_base_connection.cursor()

        data_base_cursor.execute(
            'SELECT ds_id, start_time, note '
            'FROM "Tasks" '
            'WHERE complete_status = False AND func_name = \'vac\''
        )
        vacs = data_base_cursor.fetchall()
        if not len(vacs):
            embed = discord.Embed(
                title=text['list_vac_embed_error_nobody_rest_title'],
                description=text['list_vac_embed_error_nobody_rest_description'],
                colour=discord.Colour.orange()
            )
            embed.set_image(url=text['list_vac_embed_error_nobody_rest_image'])
            await interaction.followup.send(embed=embed)
            return

        guild = self.bot.get_guild(config.dbot.privileged_guild)
        members = guild.members

        vacs = [Vac(*vac) for vac in vacs]
        vacs.sort(key=lambda vac: vac.vacation_period)

        data = ''
        for vac in vacs:
            member = get(members, id=vac.member_id)
            vacation_period = vac.vacation_period.strftime('%d.%m.%y')
            note = vac.note

            if note != 'None':
                note = f'\nПо причине:\n{note}'
            else:
                note = ''
            data += f'\n\n{member.mention} в отпуске до {vacation_period}{note}'

        embed = discord.Embed(
            title=text['list_vac_embed_title'],
            description=text['list_vac_embed_description'].format(
                data=data
            ),
            colour=discord.Colour.blue()
        )
        embed.set_image(url=text['list_vac_embed_image'])
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ListVacCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
