import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

import typing

from config import config, database


class CancelVacCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='cancel_vac', description=config.text['cancel_vac_description'])
    @app_commands.describe(target=config.text['cancel_vac_describe_target'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    async def cancel_vac(self, interaction: discord.Interaction, target: typing.Union[discord.Role, discord.Member]):

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

        if targets:
            embed = discord.Embed(
                title=config.text['cancel_vac_embed_error_no_vac_title'],
                description=config.text['cancel_vac_embed_error_no_vac_description'].format(
                    ds_users_names=', '.join([target.mention for target in targets])),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=config.text['cancel_vac_embed_error_no_vac_image'])
            await interaction.followup.send(embed=embed)

        if vacationers:
            ds_users_names = ', '.join([vacationer.mention for vacationer in vacationers])
            embed = discord.Embed(
                title=config.text['cancel_vac_embed_title'],
                description=config.text['cancel_vac_embed_description'].format(ds_users_names=ds_users_names),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=config.text['cancel_vac_embed_image'])
            await interaction.followup.send(embed=embed, content=ds_users_names)

            cursor = database.cursor()
            guild = self.bot.get_guild(config.discord_bot.privileged_guild)
            vac_role = get(guild.roles, id=config.discord_bot.vac_role)

            for vacationer in vacationers:
                await vacationer.remove_roles(vac_role)

                cursor.execute(f'DELETE FROM "Tasks" WHERE ds_id = {vacationer.id} '
                               f'AND func_name = \'unvac\' AND not complete_status')
                database.commit()

    @cancel_vac.error
    async def cancel_vac_error(self, interaction: discord.Interaction, error):
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
    await bot.add_cog(CancelVacCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
