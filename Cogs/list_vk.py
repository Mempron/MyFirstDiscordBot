import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

from config import config, database, api


class ListVKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='list_vk', description=config.text['list_vk_description'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    async def list_vk(self, interaction: discord.Interaction):
        await interaction.response.defer()

        cursor = database.cursor()

        cursor.execute('SELECT * FROM "Users"')
        data = cursor.fetchall()

        if data:
            all_users = self.bot.get_all_members()
            links = ''
            for ds_id_vk_id in data:
                ds_user = get(all_users, id=ds_id_vk_id[0])
                vk_user = await api.users.get(user_ids=ds_id_vk_id[1], name_case='ins')
                vk_user = vk_user[0]

                links += f'\nАккаунт {ds_user.mention} связан с [{vk_user.first_name} {vk_user.last_name}](https://vk.com/id{vk_user.id}).'

            embed = discord.Embed(
                title=config.text['list_vk_embed_title'],
                description=config.text['list_vk_embed_description'].format(links=links),
                colour=discord.Colour.blue()
            )
            embed.set_image(url=config.text['list_vk_embed_image'])
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title=config.text['list_vk_embed_error_nothing_in_list_title'],
                description=config.text['list_vk_embed_error_nothing_in_list_description'],
                colour=discord.Colour.orange()
            )
            embed.set_image(url=config.text['list_vk_embed_error_nothing_in_list_image'])
            await interaction.response.send_message(embed=embed)

    @list_vk.error
    async def list_vk_error(self, interaction: discord.Interaction, error):
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


async def setup(bot):
    await bot.add_cog(ListVKCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
