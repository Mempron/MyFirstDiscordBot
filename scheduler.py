from discord.ext import commands
from discord.utils import get
import discord
from pytimeparse.timeparse import timeparse

import datetime

from config import config, database


async def schedule(bot: commands.Bot):
    cursor = database.cursor()
    cursor.execute('SELECT * FROM "Tasks" WHERE complete_status = False AND start_time < NOW()')

    vac_role = get(bot.get_guild(config.discord_bot.privileged_guild).roles, id=config.discord_bot.vac_role)
    members = bot.get_all_members()
    guild = bot.get_guild(config.discord_bot.privileged_guild)
    channels = list(guild.channels)
    channels.extend(guild.threads)

    for task in cursor.fetchall():
        member = get(members, id=task[1])


        channel_id = int(task[7])
        channel = get(channels, id=channel_id)
        print(channel)
        if task[2] == 'unvac':
            await member.remove_roles(vac_role)

            embed = discord.Embed(
                title=config.text['vac_end_embed_title'],
                description=config.text['vac_end_embed_description'],
                colour=discord.Colour.purple()
            )
            embed.set_image(url=config.text['vac_end_embed_image'])
            await bot.get_channel(config.discord_bot.vac_channel).send(content=member.mention, embed=embed)
        elif task[2] == 'remind0':
            embed = discord.Embed(
                title=config.text['remind0_embed_title'],
                description=config.text['remind0_end_embed_description'].format(
                    note=task[6]
                ),
                colour=discord.Colour.brand_red()
            )
            embed.set_image(url=config.text['remind0_end_embed_image'])
            await channel.send(content=member.mention, embed=embed)
        elif task[2] == 'remind1':
            delta = datetime.timedelta(seconds=timeparse(task[3]))
            next_time = datetime.datetime.now() + delta
            embed = discord.Embed(
                title=config.text['remind1_embed_title'],
                description=config.text['remind1_end_embed_description'].format(
                    remind_id=task[0],
                    next_time=next_time.strftime('%H:%M %d.%m.%y'),
                    note=task[6]
                ),
                colour=discord.Colour.brand_red()
            )
            embed.set_image(url=config.text['remind1_end_embed_image'])
            await channel.send(content=member.mention, embed=embed)

            cursor.execute(f'UPDATE "Tasks" SET start_time = \'{next_time}\' WHERE task_id = {task[0]}')
            database.commit()
            continue
        cursor.execute(f'UPDATE "Tasks" SET complete_status = True WHERE task_id = {task[0]}')
        database.commit()
