import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

from config import config, database


class ListVacCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='list_vac', description=config.text['list_vac_description'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    async def list_vac(self, interaction: discord.Interaction):
        cursor = database.cursor()

        cursor.execute('SELECT * FROM "Tasks" WHERE complete_status = False AND func_name = \'unvac\'')
        vacs = cursor.fetchall()
        if not len(vacs):
            embed = discord.Embed(
                title=config.text['list_vac_embed_error_nobody_rest_title'],
                description=config.text['list_vac_embed_error_nobody_rest_description'],
                colour=discord.Colour.orange()
            )
            embed.set_image(url=config.text['list_vac_embed_error_nobody_rest_image'])
            await interaction.response.send_message(embed=embed)
            return

        all_users = self.bot.get_all_members()
        data = ''
        for vac in vacs:
            member = get(all_users, id=vac[1])
            vacation_period = vac[4].strftime('%d.%m.%y')
            note = vac[6]

            if note != 'None':
                note = f'\nПо причине:\n{note}'
            else:
                note = ''
            data += f'\n{member.mention} в отпуске до {vacation_period}{note}'

        embed = discord.Embed(
            title=config.text['list_vac_embed_title'],
            description=config.text['list_vac_embed_description'].format(
                data=data
            ),
            colour=discord.Colour.blue()
        )
        embed.set_image(url=config.text['list_vac_embed_image'])
        await interaction.response.send_message(embed=embed)

    @list_vac.error
    async def list_vac_error(self, interaction: discord.Interaction, error):
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
    await bot.add_cog(ListVacCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
