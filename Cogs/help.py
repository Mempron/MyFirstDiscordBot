import discord
from discord import app_commands
from discord.ext import commands

from config import config


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description=config.text['help_description'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour=discord.Colour.gold(),
            title=config.text['help_embed_title'].format(ds_user_name=interaction.user.name),
            description=config.text['help_embed_description'],
            url=config.text['help_embed_url']
        )
        embed.set_image(url=config.text['help_embed_image'])
        await interaction.response.send_message(embed=embed)

    @help.error
    async def help_error(self, interaction: discord.Interaction, error):
        print(error)
        if isinstance(error, discord.app_commands.errors.MissingAnyRole):
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=config.text['error_embed_title'],
                description=config.text['error_embed_description'].format(name=interaction.user.name),
            )
            embed.set_image(url=config.text['error_embed_image'])
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
