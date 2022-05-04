from discord.ext import commands
import psycopg2

from config import get_config


class RemindCancelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='remind_cancel')
    async def remind_cancel(self, ctx, task_id):
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
            if len(cursor_data) == 0:
                await ctx.send('Напоминаний нет.')
                return
            for task in cursor_data:
                if task_id == 'все' or task[0] == int(task_id):
                    cursor.execute(
                        f'UPDATE "Tasks" SET complete_status = True WHERE ds_id = {ctx.author.id} AND (func_name = \'remind0\' OR func_name = \'remind1\') AND not complete_status')
                    connection.commit()
                    await ctx.send(f'Напоминание под номером {task[0]} отменено.')
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='help_remind_cancel')
    async def help_remind_cancel(self, ctx):
        await ctx.send(
            'Формат команды:\nremind_cancel id (Номер напоминания или "все", чтобы отменить все напоминания)')


async def setup(bot):
    await bot.add_cog(RemindCancelCog(bot))
