import discord
from discord.ext import commands
from discord import app_commands

from asyncio import sleep

from config import get_config
from scheduler import schedule

config = get_config()
intents = discord.Intents(messages=True, guilds=True, members=True, message_content=True)

cogs = [
    'help',
    'vac',
    'unvac',
    'vac_list',
    'remind',
    'remind_cancel',
    'remind_list',
    'ping',
    'test',
    'vk_add'
]

bot = commands.Bot(intents=intents, command_prefix='*')
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='... Нет, я не играю!\nЯ усердно работаю!'))
    for cog in cogs:
        await bot.load_extension(f'Cogs.{cog}')

    print(bot.guilds[0])
    await bot.tree.sync(guild=bot.guilds[0])


    while True:
        await schedule(bot)
        await sleep(30)


bot.run(config.discord_bot.token)
