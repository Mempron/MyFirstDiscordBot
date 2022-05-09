import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

import typing
from datetime import datetime, date

from config import config, database, api


class VacVKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='vac', description=config.text['vac_description'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.describe(target=config.text['vac_describe_target'],
                           note=config.text['vac_describe_note'],
                           vacation_period=config.text['vac_describe_date'])
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    async def vac(self, interaction: discord.Interaction, target: typing.Union[discord.Role, discord.Member],
                  vacation_period: str,
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
            ds_users_names = ', '.join([vacationer.mention for vacationer in vacationers])
            embed = discord.Embed(
                title=config.text['vac_embed_error_vac_already_title'],
                description=config.text['vac_embed_vac_already_description'].format(
                    ds_users_names=ds_users_names
                ),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=config.text['vac_embed_vac_already_image'])

            await interaction.followup.send(embed=embed)

        if targets:
            embed = discord.Embed(
                title=config.text['vac_embed_error_vacation_period_title'],
                description=config.text['vac_embed_error_vacation_period_description'].format(
                    vacation_period=vacation_period
                ),
                colour=discord.Colour.red()
            )
            embed.set_image(url=config.text['vac_embed_error_vacation_period_image'])
            try:
                if datetime.strptime(vacation_period, '%d.%m.%Y').date() < date.today():
                    await interaction.followup.send(embed=embed)
                    return
            except ValueError:
                await interaction.followup.send(embed=embed)
                return

            ds_users_names = ', '.join([ds_user.mention for ds_user in targets])
            new_note = None
            if note is None:
                new_note = ''
            else:
                new_note = f'\nПо причине:\n{note}'

            embed = discord.Embed(
                title=config.text['vac_embed_title'],
                description=config.text['vac_embed_description'].format(
                    ds_users_names=ds_users_names,
                    vacation_period=vacation_period,
                    note=new_note
                ),
                colour=discord.Colour.blurple()
            )
            embed.set_image(url=config.text['vac_embed_image'])
            await interaction.followup.send(embed=embed, content=ds_users_names)

            cursor = database.cursor()
            guild = self.bot.get_guild(config.discord_bot.privileged_guild)
            vac_role = get(guild.roles, id=config.discord_bot.vac_role)
            for target in targets:
                await target.add_roles(vac_role)
                cursor.execute(f'INSERT INTO "Tasks" (ds_id, func_name, note, start_time, complete_status) VALUES '
                               f'({target.id}, \'unvac\', \'{note}\', \'{vacation_period}\', False)')
                database.commit()

    @vac.error
    async def vac_error(self, interaction: discord.Interaction, error):
        print(error)
        print(type(error))
        print(error.original)
        print(type(error.original))
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


async def setup(bot):
    await bot.add_cog(VacVKCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
