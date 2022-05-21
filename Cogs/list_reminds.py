import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import psycopg2

from config import config
from text import text
from task import Task


class ListRemindsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='list_reminds', description=text['list_reminds_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    async def list_reminds(self, interaction: discord.Interaction):

        await interaction.response.defer()

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
            'WHERE complete_status = False AND (func_name = \'remind0\' OR func_name = \'remind1\')')

        reminds = [Task(*remind) for remind in data_base_cursor.fetchall()]

        data_base_cursor.close()
        data_base_connection.close()

        if reminds:
            guild = self.bot.get_guild(config.dbot.privileged_guild)
            channels = list(self.bot.get_all_channels())
            channels.extend(guild.threads)

            for remind in reminds:

                ds_user = self.bot.get_user(remind.ds_id)
                channel = get(channels, id=remind.source)

                repeat = int(remind.func_name[-1])
                if repeat:
                    repeat = 'Да'
                else:
                    repeat = 'Нет'

                embed = discord.Embed(
                    title=text['list_reminds_embed_title'].format(remind_id=remind.id),
                    description=text['list_reminds_embed_description'].format(
                        ds_user_name=ds_user.mention,
                        repeat=repeat,
                        channel_name=channel.mention,
                        timedelta=remind.func_args,
                        next_time=remind.start_time.strftime('%H:%M %d.%m.%y'),
                        note=remind.note
                    ),
                    colour=discord.Colour.random()
                )
                embed.set_image(url=text['list_reminds_embed_image'])
                await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                title=text['list_reminds_embed_error_no_reminds_title'],
                description=text['list_reminds_embed_no_reminds_description'],
                colour=discord.Colour.orange()
            )
            embed.set_image(url=text['list_reminds_embed_no_reminds_image'])
            await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ListRemindsCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
