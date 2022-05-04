from discord.ext import commands
import psycopg2

from config import get_config


class RemindListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='remind_list')
    async def remind_list(self, ctx):
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

            cursor.execute(f'SELECT * FROM "Tasks" WHERE ds_id = {ctx.author.id} AND complete_status = False')
            cursor_data = cursor.fetchall()

            if not len(cursor_data):
                await ctx.send('Напоминаний нет.')
                return

            for task in cursor_data:
                await ctx.send(
                    f'ID: {task[0]}\nСледующее напоминание будет: {task[4].strftime("%H:%M %d.%m.%y")}\nНапоминание:\n{task[6]}')
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


async def setup(bot):
    await bot.add_cog(RemindListCog(bot))
