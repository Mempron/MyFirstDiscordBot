from discord.ext import commands
from discord.utils import get
import psycopg2
from pytimeparse.timeparse import timeparse

import datetime

from config import get_config


async def schedule(bot: commands.Bot):
    config = get_config()

    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host=config.data_base.host,
            port=config.data_base.port,
            database=config.data_base.name,
            user=config.data_base.user,
            password=config.data_base.password
        )
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM "Tasks" WHERE complete_status = False AND start_time < NOW()')

        vac_role = get(bot.get_guild(config.discord_bot.privileged_guild).roles, id=config.discord_bot.vac_role)
        members = bot.get_all_members()
        channels = list(bot.get_all_channels())
        channels.extend(bot.guilds[0].threads)

        for task in cursor.fetchall():
            member = get(members, id=task[1])

            if task[2] == 'unvac':
                await member.remove_roles(vac_role)
                await bot.get_channel(config.discord_bot.vac_channel).send(f'Отпуск {member.mention} окончен.')
            elif task[2] == 'remind0':
                await bot.get_channel(int(task[7])).send(f'{member.mention}\n{task[6]}')
            elif task[2] == 'remind1':
                await bot.get_channel(int(task[7])).send(f'{member.mention}\nID: {task[0]}\n{task[6]}')
                delta = datetime.timedelta(seconds=timeparse(task[3]))
                cursor.execute(f'UPDATE "Tasks" SET start_time = \'{task[4] + delta}\' WHERE task_id = {task[0]}')
                connection.commit()
                continue
            cursor.execute(f'UPDATE "Tasks" SET complete_status = True WHERE task_id = {task[0]}')
            connection.commit()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
