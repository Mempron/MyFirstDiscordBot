import discord
from discord.ext import commands
from discord.utils import get
from vkbottle import API

from random import randint
import typing

from config import get_config


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='ping')
    async def ping(self, ctx, target: typing.Union[discord.Role, discord.Member], *, note):
        config = get_config()

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

        api = API(config.vk_bot.token)
        peers = ''
        i = 1
        for target in targets:
            await ctx.send(f'Пинг {target.name} был успешно отправлен.')
            peers += target.name
            if not i == len(targets):
                peers += ', '
            i += 1

        # 2000000002
        await api.messages.send(peer_id=2000000002, random_id=randint(0, 100000),
                                message=f'Внимание: {peers}!\nНазвание канала или ветки: {ctx.message.channel.parent}\n{note}')

    @commands.has_any_role(910608186896175114, 910991296301256744, 910607573747650643, 911036330459418634)
    @commands.command(name='help_ping')
    async def help_ping(self, ctx):
        await ctx.send('Формат команды:\nping @имя, @роль или имя#цифры Текст\nПример команды:\nping '
                       'tenshich#4444 Мы доделали задачи в этой ветке')


async def setup(bot):
    await bot.add_cog(PingCog(bot))
