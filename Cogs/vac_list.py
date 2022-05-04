from discord.ext import commands
from discord.utils import get
import psycopg2

from config import get_config


class VacListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='vac_list')
    async def vac_list(self, ctx):
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

            cursor.execute('SELECT * FROM "Tasks" WHERE complete_status = False AND func_name = \'unvac\'')

            vacs = cursor.fetchall()
            if not len(vacs):
                await ctx.send('В отпуске никого нет.')
                return
            for vac in vacs:
                member = get(ctx.guild.members, id=vac[1])
                date = vac[4].strftime('%d.%m.%y')
                await ctx.send(f'{member.name} в отпуске до {date}\nКомментарий:\n{vac[6]}')

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


async def setup(bot):
    await bot.add_cog(VacListCog(bot))
