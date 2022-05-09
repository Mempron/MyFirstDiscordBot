import asyncio

import discord
from discord.ext import commands

import logging

from config import config
from scheduler import schedule

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='&`',
            intents=intents,
            application_id=config.discord_bot.application_id,
        )

    async def setup_hook(self) -> None:
        for cog in config.discord_bot.cogs:
            await self.load_extension(f'Cogs.{cog}')
        await self.tree.sync(guild=discord.Object(config.discord_bot.privileged_guild))


async def main():
    await bot.start(config.discord_bot.token)


bot = MyBot()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='русскую рулетку!'))
    while True:
        await schedule(bot)
        await asyncio.sleep(60)


asyncio.run(main())
