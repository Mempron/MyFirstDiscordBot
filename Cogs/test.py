import discord
from discord.ext import commands
from discord.utils import get
import psycopg2


class EmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='embed')
    async def embed(self, ctx):
        embed = discord.Embed(title="Напоминание",
                              description="Посмотреть серию любимого аниме @Mempron",
                              color=0x8C3EED)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(EmbedCog(bot))
