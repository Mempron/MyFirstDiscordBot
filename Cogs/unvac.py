import discord
from discord.ext import commands
from discord.utils import get
import psycopg2

import typing

from config import get_config


class UnVacCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='unvac')
    async def unvac(self, ctx, target: typing.Union[discord.Role, discord.Member]):
        config = get_config()

        targets = []
        if isinstance(target, discord.role.Role):
            targets.extend(target.members)
        elif isinstance(target, discord.member.Member):
            targets.append(target)

        vac_role = get(ctx.guild.roles, id=config.discord_bot.vac_role)
        if not vac_role:
            await ctx.send('Не могу найти роль отпуска.\nНапишете Mempron#5630')

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
                if vac_role not in target.roles:
                    await ctx.send(f'{target.name} и так не в отпуске.')
                    continue
                await target.remove_roles(vac_role)
                await ctx.send(f'Отпуск {target.mention} окончен.')
                cursor.execute(
                    f'UPDATE "Tasks" SET complete_status = True WHERE ds_id = {target.id} AND func_name = \'unvac\' AND not complete_status')
                connection.commit()
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='help_unvac')
    async def help_unvac(self, ctx):
        await ctx.send('Формат команды:\nunvac @имя, @роль или имя#цифры\nК примеру:\nunvac @Mempron')


async def setup(bot):
    await bot.add_cog(UnVacCog(bot))
