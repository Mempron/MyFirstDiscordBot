import discord
from discord.ext import commands
from discord.utils import get
from pytimeparse.timeparse import timeparse
import psycopg2

import asyncio
import datetime

from config import config
from text import text
from task import Task
from tree import MyTree


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='&',
            intents=discord.Intents.all(),
            application_id=config.dbot.application_id,
            tree_cls=MyTree
        )

    async def setup_hook(self) -> None:
        for cog in config.dbot.cogs:
            await self.load_extension(f'Cogs.{cog}')

    async def on_ready(self):
        await self.schedule()

    async def schedule(self):
        while True:
            guild = self.get_guild(config.dbot.privileged_guild)
            vacation_role = get(guild.roles, id=config.dbot.vac_role)
            channels = list(guild.channels)
            channels.extend(guild.threads)
            members = guild.members

            data_base_connection = psycopg2.connect(
                host=config.db.host,
                port=config.db.port,
                database=config.db.name,
                user=config.db.user,
                password=config.db.password
            )
            data_base_cursor = data_base_connection.cursor()

            data_base_cursor.execute(
                'SELECT task_id, ds_id, func_name, func_args, start_time, note, source '
                'FROM "Tasks" '
                'WHERE complete_status = False AND start_time < NOW()'
            )

            tasks = [Task(*task) for task in data_base_cursor.fetchall()]

            if tasks:
                for task in tasks:
                    member = get(members, id=task.ds_id)
                    channel = get(channels, id=task.source)

                    match task.func_name:
                        case 'vac':
                            await member.remove_roles(vacation_role)

                            embed = discord.Embed(
                                title=text['vac_end_embed_title'],
                                description=text['vac_end_embed_description'],
                                colour=discord.Colour.purple()
                            )
                            embed.set_image(url=text['vac_end_embed_image'])
                            await channel.send(content=member.mention, embed=embed)

                        case 'remind0':
                            embed = discord.Embed(
                                title=text['remind0_embed_title'],
                                description=text['remind0_end_embed_description'].format(
                                    note=task.note
                                ),
                                colour=discord.Colour.brand_red()
                            )
                            embed.set_image(url=text['remind0_end_embed_image'])
                            await channel.send(content=member.mention, embed=embed)

                        case 'remind1':
                            delta = datetime.timedelta(seconds=timeparse(task.func_args))
                            next_time = datetime.datetime.now() + delta
                            embed = discord.Embed(
                                title=text['remind1_embed_title'],
                                description=text['remind1_end_embed_description'].format(
                                    remind_id=task.id,
                                    next_time=next_time.strftime('%H:%M %d.%m.%y'),
                                    note=task.note
                                ),
                                colour=discord.Colour.brand_red()
                            )
                            embed.set_image(url=text['remind1_end_embed_image'])
                            await channel.send(content=member.mention, embed=embed)

                            data_base_cursor.execute(
                                f'UPDATE "Tasks" SET start_time = \'{next_time}\' WHERE task_id = {task.id}')
                            data_base_connection.commit()

                            continue

                        case _:
                            embed = discord.Embed(
                                title=f'Задача: {task.id}',
                                description=f'Неизвестная мне команда: {task.func_name}\n'
                                            f'Аргументы: {task.func_args}\n'
                                            f'Когда: {task.start_time}\n'
                                            f'Откуда: {channel.mention}'
                            )
                            await channel.send(content=member.mention, embed=embed)

                    data_base_cursor.execute(f'DELETE FROM "Tasks" WHERE task_id = {task.id}')
                    data_base_connection.commit()

            data_base_cursor.close()
            data_base_connection.close()

            await asyncio.sleep(60)
