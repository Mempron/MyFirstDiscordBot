import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

from config import config, database


class ListRemindsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='list_reminds', description=config.text['list_reminds_description'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    async def list_reminds(self, interaction: discord.Interaction):
        await interaction.response.defer()
        cursor = database.cursor()
        cursor.execute('SELECT * FROM "Tasks" WHERE complete_status = False AND (func_name = \'remind0\' '
                       'OR func_name = \'remind1\')')

        data = cursor.fetchall()
        if data:
            guild = self.bot.get_guild(config.discord_bot.privileged_guild)
            channels = list(self.bot.get_all_channels())
            channels.extend(guild.threads)
            for row in data:
                remind_id = int(row[0])
                ds_id = int(row[1])
                repeat = int(row[2][-1])
                timedelta = row[3]
                next_time = row[4]
                note = row[6]
                channel_id = int(row[7])

                ds_user = self.bot.get_user(ds_id)
                channel = get(channels, id=channel_id)

                if repeat:
                    repeat = 'Да'
                else:
                    repeat = 'Нет'

                channel_name = channel.name

                try:
                    if channel.parent:
                        channel_name = channel.parent.name + ' \u2192 ' + channel_name
                except AttributeError:
                    pass

                embed = discord.Embed(
                    title=config.text['list_reminds_embed_title'].format(remind_id=remind_id),
                    description=config.text['list_reminds_embed_description'].format(
                        ds_user_name=ds_user.mention,
                        repeat=repeat,
                        channel_name=channel_name,
                        timedelta=timedelta,
                        next_time=next_time.strftime('%H:%M %d.%m.%y'),
                        note=note
                    ),
                    colour=discord.Colour.random()
                )
                embed.set_image(url=config.text['list_reminds_embed_image'])
                await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                title=config.text['list_reminds_embed_error_no_reminds_title'],
                description=config.text['list_reminds_embed_no_reminds_description'],
                colour=discord.Colour.orange()
            )
            embed.set_image(url=config.text['list_reminds_embed_no_reminds_image'])
            await interaction.followup.send(embed=embed)

    @list_reminds.error
    async def remind_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.MissingAnyRole):
            embed = discord.Embed(
                title=config.text['embed_error_missing_any_role_title'],
                description=config.text['embed_error_missing_any_role_description'].format(
                    ds_user_name=interaction.user.name),
                colour=discord.Colour.red()
            )
            embed.set_image(url=config.text['embed_error_missing_any_role_image'])
            await interaction.followup.send(embed=embed)
            return

        error_text = f'{type(error)}\n{error}'
        if error.original:
            error_text += f'\n{type(error.original)}\n{error.original}'

        embed = discord.Embed(
            title=config.text['unknown_error_embed_title'],
            description=config.text['unknown_error_embed_description'].format(error=error_text),
            colour=discord.Colour.red()
        )
        embed.set_image(url=config.text['unknown_error_embed_image'])
        await interaction.followup.send(embed=embed)

        print('Хьюстон, у нас проблема!')
        print(f'{interaction.user.name} натворил делов!')

        print('---------------------')
        print(f'Type of Error: {type(error)}')
        print(f'Error: {error}')
        if error.original:
            print('---------------------')
            print('Which contains another error:')
            print(f'Type of Error: {type(error.original)}')
            print(f'Error: {error.original}')


async def setup(bot):
    await bot.add_cog(ListRemindsCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
