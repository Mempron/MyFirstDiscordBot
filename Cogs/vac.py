import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import psycopg2

import typing
from datetime import datetime, date

from config import config
from text import text
from Utils.get_targets import get_targets


class VacVKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='vac', description=text['vac_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.describe(
        targets=text['vac_describe_target'],
        note=text['vac_describe_note'],
        vacation_period=text['vac_describe_date']
    )
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    async def vac(
            self,
            interaction: discord.Interaction,
            targets: typing.Union[discord.Role, discord.Member],
            vacation_period: str,
            note: str = None
    ):
        await interaction.response.defer()

        targets = await get_targets(interaction, targets)

        if targets:
            try:
                if datetime.strptime(vacation_period, '%d.%m.%Y').date() < date.today():
                    raise ValueError
            except ValueError:
                embed = discord.Embed(
                    title=text['vac_embed_error_vacation_period_title'],
                    description=text['vac_embed_error_vacation_period_description'].format(
                        vacation_period=vacation_period
                    ),
                    colour=discord.Colour.red()
                )
                embed.set_image(url=config.text['vac_embed_error_vacation_period_image'])
                await interaction.followup.send(embed=embed)
                return

            ds_users_names = ', '.join([ds_user.mention for ds_user in targets])

            format_note = None
            if note is None:
                format_note = ''
            else:
                format_note = f'\nПо причине:\n{note}'

            embed = discord.Embed(
                title=text['vac_embed_title'],
                description=text['vac_embed_description'].format(
                    ds_users_names=ds_users_names,
                    vacation_period=vacation_period,
                    note=format_note
                ),
                colour=discord.Colour.blurple()
            )
            embed.set_image(url=text['vac_embed_image'])
            await interaction.followup.send(embed=embed, content=ds_users_names)

            guild = self.bot.get_guild(config.dbot.privileged_guild)
            vacation_role = get(guild.roles, id=config.dbot.vac_role)

            data_base_connection = psycopg2.connect(
                host=config.db.host,
                port=config.db.port,
                database=config.db.name,
                user=config.db.user,
                password=config.db.password
            )
            data_base_cursor = data_base_connection.cursor()

            vacation_period = datetime.strptime(vacation_period, '%d.%m.%Y')
            for target in targets:
                await target.add_roles(vacation_role)
                data_base_cursor.execute(
                    f'INSERT INTO "Tasks" '
                    f'(ds_id, func_name, note, start_time, complete_status, source) '
                    f'VALUES '
                    f'({target.id}, \'vac\', \'{note}\', \'{vacation_period}\', False, {config.dbot.vac_channel})')
                data_base_connection.commit()

            data_base_cursor.close()
            data_base_connection.close()


async def setup(bot):
    await bot.add_cog(VacVKCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
