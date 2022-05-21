import discord
from discord import app_commands
from discord.ext import commands

from config import config
from text import text


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description=text['help_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    async def help(
            self,
            interaction: discord.Interaction
    ):
        await interaction.response.defer()

        embed = discord.Embed(
            colour=discord.Colour.gold(),
            title=text['help_embed_title'].format(ds_user_name=interaction.user.name),
            description=text['help_embed_description']
        )
        embed.set_image(url=text['help_embed_image'])
        await interaction.followup.send(embed=embed)
        # await self.bot.tree.sync(guild=discord.Object(config.dbot.privileged_guild))


async def setup(bot):
    await bot.add_cog(HelpCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
