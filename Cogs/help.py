from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.send('Я могу следующее:\nvac — отправить в отпуск\nunvac — вернуть из отпуска\nvac_list — все те, кто в отпуске\nping '
                       '— пинг в вк\nremind — создать напоминание\nremind_cancel — отменить напоминание\nremind_list '
                       '— список напоминаний')


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
