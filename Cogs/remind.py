import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import psycopg2

import typing
import datetime

from config import config
from text import text
from Utils.get_targets import get_targets


class RemindCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='remind', description=text['remind_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    @app_commands.describe(
        target=text['remind_describe_target'],
        repeat=text['remind_describe_repeat'],
        raw_time_delta=text['remind_describe_next_time'],
        note=text['remind_describe_note']
    )
    @app_commands.choices(repeat=[
        Choice(name='один раз', value=0),
        Choice(name='много раз', value=1)
    ])
    async def remind(self,
                     interaction: discord.Interaction,
                     target: typing.Union[discord.Role, discord.Member],
                     repeat: Choice[int],
                     raw_time_delta: str,
                     note: str
                     ):

        await interaction.response.defer()

        targets = await get_targets(interaction, target)

        if targets:

            now = datetime.datetime.now()
            timedelta = datetime.timedelta(seconds=0)
            raw_time_delta = raw_time_delta.split(' ')
            for value in raw_time_delta:
                match value[-1]:
                    case 'н':
                        timedelta += datetime.timedelta(weeks=int(value[:-1]))
                    case 'д':
                        timedelta += datetime.timedelta(days=int(value[:-1]))
                    case 'ч':
                        timedelta += datetime.timedelta(hours=int(value[:-1]))
                    case 'м':
                        timedelta += datetime.timedelta(minutes=int(value[:-1]))
            if timedelta == datetime.timedelta(seconds=0):
                raise ValueError

            next_time = now + timedelta

            embed = discord.Embed(
                title=text['remind_embed_title'],
                description=text['remind_embed_description'].format(
                    repeat=repeat.name,
                    ds_users_names=', '.join([target.mention for target in targets]),
                    raw_time_delta=' '.join(raw_time_delta),
                    next_time=next_time.strftime('%H:%M %d.%m.%y'),
                    note=note
                ),
                colour=discord.Colour.blue()
            )
            embed.set_image(url=text['remind_embed_title_image'])
            await interaction.followup.send(embed=embed)

            data_base_connection = psycopg2.connect(
                host=config.db.host,
                port=config.db.port,
                database=config.db.name,
                user=config.db.user,
                password=config.db.password
            )
            data_base_cursor = data_base_connection.cursor()

            for target in targets:
                data_base_cursor.execute(
                    f'INSERT INTO "Tasks" '
                    f'(ds_id, func_name, func_args, start_time, complete_status, note, source) '
                    f'VALUES '
                    f'({target.id}, '
                    f'\'remind{str(repeat.value)}\', '
                    f'\'{timedelta}\', '
                    f'\'{next_time}\', '
                    f'False, '
                    f'\'{note}\', '
                    f'\'{interaction.channel_id}\')')
                data_base_connection.commit()

            data_base_cursor.close()
            data_base_connection.close()

    @remind.error
    async def remind_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandInvokeError):
            if isinstance(error.original, ValueError):
                embed = discord.Embed(
                    title=text['remind_embed_error_value_title'],
                    description=text['remind_embed_error_value_description'].format(
                        raw_time_delta=interaction.namespace.raw_time_delta),
                    colour=discord.Colour.red()
                )
                embed.set_image(url=text['remind_embed_error_value_title_image'])
                await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RemindCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
