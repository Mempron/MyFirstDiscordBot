import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import psycopg2

from config import config
from text import text
from task import Task


class CancelRemindCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='cancel_remind', description=text['cancel_reminds_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.describe(remind_id=text['cancel_reminds_describe_remind_id'])
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    async def cancel_remind(self, interaction: discord.Interaction, remind_id: int):
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
            f'DELETE FROM "Tasks" '
            f'WHERE task_id = {remind_id} AND (func_name = \'remind0\' OR func_name = \'remind1\')'
            f'RETURNING task_id, ds_id, func_name, func_args, start_time, note, source')
        data_base_connection.commit()

        response = data_base_cursor.fetchone()

        data_base_cursor.close()
        data_base_connection.close()

        if response:
            guild = self.bot.get_guild(config.dbot.privileged_guild)
            channels = list(self.bot.get_all_channels())
            channels.extend(guild.threads)

            remind = Task(*response)

            ds_user = self.bot.get_user(remind.ds_id)
            channel = get(channels, id=remind.source)

            repeat = int(remind.func_name[-1])
            if repeat:
                repeat = 'Да'
            else:
                repeat = 'Нет'

            embed = discord.Embed(
                title=text['cancel_reminds_embed_title'],
                description=text['cancel_reminds_embed_description'].format(
                    remind_id=remind_id,
                    ds_user_name=ds_user.mention,
                    repeat=repeat,
                    channel_name=channel.mention,
                    timedelta=remind.func_args,
                    next_time=remind.start_time.strftime('%H:%M %d.%m.%y'),
                    note=remind.note
                ),
                colour=discord.Colour.random()
            )
            embed.set_image(url=text['cancel_reminds_embed_image'])
            await interaction.followup.send(embed=embed)

        else:
            embed = discord.Embed(
                title=text['cancel_reminds_embed_error_no_reminds_title'],
                description=text['cancel_reminds_reminds_embed_no_reminds_description'].format(
                    remind_id=remind_id
                ),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=text['cancel_reminds_reminds_embed_no_reminds_image'])
            await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CancelRemindCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
