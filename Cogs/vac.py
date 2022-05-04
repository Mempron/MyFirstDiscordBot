import discord
from discord.ext import commands
from discord.utils import get
import psycopg2

from datetime import datetime, date
import typing

from config import get_config


class VacCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='vac')
    async def vac(self, ctx, target: typing.Union[discord.Role, discord.Member], vacation_period, *, note):
        config = get_config()

        if datetime.strptime(vacation_period, '%d.%m.%Y').date() < date.today():
            await ctx.send(f'Неверная дата окончания отпуска: {vacation_period}')
            return

        targets = []
        if isinstance(target, discord.role.Role):
            targets.extend(target.members)
        elif isinstance(target, discord.member.Member):
            targets.append(target)

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
            vac_role = get(ctx.guild.roles, id=config.discord_bot.vac_role)




            if not vac_role:
                await ctx.send('Не могу найти роль отпуска.\nНапишете Mempron#5630')
            for target in targets:
                if get(target.roles, id=config.discord_bot.vac_role):
                    await ctx.send(f'{target} и так уже в отпуске.')
                    continue
                await target.add_roles(vac_role)
                await ctx.send(f'Теперь {target} в отпуске до {vacation_period}.\nКомментарий:\n{note}')
                embed = discord.Embed(title="Напоминание", url='https://www.youtube.com/c/NotADub',
                                      description=f"""> dawdawdawd Посмотреть серию любимого аниме {target.mention} Практический опыт показывает, что социально-экономическое развитие напрямую зависит от всесторонне сбалансированных нововведений. Разнообразный и богатый опыт постоянное информационно-техническое обеспечение нашей деятельности напрямую зависит от новых предложений. Не следует, однако, забывать о том, что социально-экономическое развитие играет важную роль в формировании соответствующих условий активизации.

Соображения высшего порядка, а также начало повседневной работы по формированию позиции играет важную роль в формировании всесторонне сбалансированных нововведений. Таким образом, дальнейшее развитие различных форм деятельности влечет за собой процесс внедрения и модернизации модели развития? Дорогие друзья, начало повседневной работы по формированию позиции влечет за собой процесс внедрения и модернизации всесторонне сбалансированных нововведений. Задача организации, в особенности же повышение уровня гражданского сознания позволяет оценить значение позиций, занимаемых участниками в отношении поставленных задач.

Равным образом реализация намеченного плана развития играет важную роль в формировании существующих финансовых и административных условий. Не следует, однако, забывать о том, что повышение уровня гражданского сознания позволяет выполнить важнейшие задания по разработке всесторонне сбалансированных нововведений? Практический опыт показывает, что постоянный количественный рост и сфера нашей активности напрямую зависит от модели развития. Соображения высшего порядка, а также постоянный количественный рост и сфера нашей активности позволяет оценить значение существующих финансовых и административных условий?

Соображения высшего порядка, а также консультация с профессионалами из IT в значительной степени...""",
                                      color=0x8C3EED)
                await ctx.send(embed=embed)

                cursor.execute(f'INSERT INTO "Tasks" (ds_id, func_name, note, start_time, complete_status) VALUES '
                               f'({target.id}, \'unvac\', \'{note}\', \'{vacation_period}\', False)')
                connection.commit()

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='help_vac')
    async def help_vac(self, ctx):
        await ctx.send('Формат команды:\nvac @имя, @роль или имя#цифры дд.мм.год комментарий\nК примеру:\nvac '
                       '@Mempron 14.12.2077 Приятного тебе отдыха')


async def setup(bot):
    await bot.add_cog(VacCog(bot))
