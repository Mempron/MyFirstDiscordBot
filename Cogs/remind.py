import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from discord.app_commands import Choice

import typing
import datetime

from config import config, database


class RemindCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='remind', description=config.text['remind_description'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    @app_commands.describe(
        target=config.text['remind_describe_target'],
        repeat=config.text['remind_describe_repeat'],
        raw_time_delta=config.text['remind_describe_next_time'],
        note=config.text['remind_describe_note']
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
                title=config.text['remind_embed_title'],
                description=config.text['remind_embed_description'].format(
                    repeat=repeat.name,
                    ds_users_names=', '.join([target.mention for target in targets]),
                    raw_time_delta=' '.join(raw_time_delta),
                    next_time=next_time.strftime('%H:%M %d.%m.%y'),
                    note=note
                ),
                colour=discord.Colour.blue()
            )
            embed.set_image(url=config.text['remind_embed_title_image'])
            await interaction.followup.send(embed=embed)

            cursor = database.cursor()

            for target in targets:
                cursor.execute(f'INSERT INTO "Tasks" (ds_id, func_name, func_args, start_time, complete_status, note, '
                               f'source) VALUES ({target.id}, \'remind{str(repeat.value)}\', '
                               f'\'{timedelta}\', \'{next_time}\', False, \'{note}\', '
                               f'\'{interaction.channel_id}\')')
                database.commit()

    @remind.error
    async def remind_error(self, interaction: discord.Interaction, error):
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

        elif isinstance(error, app_commands.errors.CommandInvokeError):
            if isinstance(error.original, ValueError):
                embed = discord.Embed(
                    title=config.text['remind_embed_error_value_title'],
                    description=config.text['remind_embed_error_value_description'].format(
                        raw_time_delta=interaction.namespace.raw_time_delta),
                    colour=discord.Colour.red()
                )
                embed.set_image(url=config.text['remind_embed_error_value_title_image'])
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
    await bot.add_cog(RemindCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
