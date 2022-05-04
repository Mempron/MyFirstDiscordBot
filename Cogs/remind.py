import discord
from discord.ext import commands
from discord.utils import get
import psycopg2

import typing
import datetime

from config import get_config


class RemindCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='remind')
    async def remind(self, ctx, target: typing.Union[discord.Role, discord.Member], repeat: bool, *, data):
        config = get_config()

        time = data[:data.find('(')]
        text = data[data.find('(') + 1: -1]

        targets = []
        if isinstance(target, discord.role.Role):
            for member in target.members:
                vac_role = get(member.roles, id=config.discord_bot.vac_role)
                if vac_role:
                    await ctx.send(f'Не стоит беспокоить человека в отпуске: {target.name}')
                    continue
                targets.append(member)
        elif isinstance(target, discord.member.Member):
            vac_role = get(target.roles, id=config.discord_bot.vac_role)
            if vac_role:
                await ctx.send(f'Не стоит беспокоить человека в отпуске: {target.name}')
                return
            targets.append(target)

        now = datetime.datetime.now()
        timedelta = datetime.timedelta(seconds=0)
        if 'м' in time:
            delta = int(time[time.find('м') - 1])
            timedelta += datetime.timedelta(minutes=delta)
        if 'ч' in time:
            delta = int(time[time.find('ч') - 1])
            timedelta += datetime.timedelta(hours=delta)
        if 'д' in time:
            delta = int(time[time.find('д') - 1])
            timedelta += datetime.timedelta(days=delta)
        if 'М' in time:
            delta = int(time[time.find('М') - 1]) * 31
            timedelta += datetime.timedelta(days=delta)
        if 'г' in time:
            delta = int(time[time.find('г') - 1]) * 365
            timedelta += datetime.timedelta(days=delta)
        if not timedelta > datetime.timedelta(minutes=0):
            await ctx.send(f'Не могу понять через какое время надо напомнить: {time}')

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

            for target in targets:
                await ctx.send(f'Напоминание {target.name} будет доставлено')
                cursor.execute(f'INSERT INTO "Tasks" (ds_id, func_name, func_args, start_time, complete_status, note, '
                               f'source) VALUES ({target.id}, \'remind{int(repeat)}\', '
                               f'\'{timedelta}\', \'{now + timedelta}\', False, \'{text}\', '
                               f'\'{ctx.message.channel.id}\')')
                connection.commit()
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='help_remind')
    async def help_remind(self, ctx):
        await ctx.send('Формат команды:\nremind (@человек, @роль или кому#цифры) (0 - не повторять или 1 - '
                       'повторять) (0г(оды) 0М(есяца) 0н(едели) 0д(ни) 0ч(асы) 0м(инуты) (напоминание)\nК '
                       'примеру:\nremind @Mempron 1 1д (Не забыть посмотреть серию любимого аниме!)')


async def setup(bot):
    await bot.add_cog(RemindCog(bot))
