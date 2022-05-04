import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from discord.utils import get
from vkbottle import API

from random import randint
import typing

from config import get_config

config = get_config()


class VkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.guilds(433504483054452746)
    @app_commands.command(name='fruit')
    @app_commands.describe(fruits='fruits to choose from')
    @app_commands.choices(fruits=[
        Choice(name='apple', value=1),
        Choice(name='banana', value=2),
        Choice(name='cherry', value=3),
    ])
    async def fruit(self, interaction: discord.Interaction, fruits: Choice[int]):
        await interaction.response.send_message(f'Your favourite fruit is {fruits.name}.')


async def setup(bot):
    await bot.add_cog(VkCog(bot))
