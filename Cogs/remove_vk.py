import discord
from discord import app_commands
from discord.ext import commands
import psycopg2
import vkbottle
from vkbottle import VKAPIError

from random import randint

from config import config
from text import text


class RemoveVKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='remove_vk', description=text['remove_vk_description'])
    @app_commands.guilds(config.dbot.privileged_guild)
    @app_commands.checks.has_any_role(*config.dbot.privileged_roles)
    @app_commands.describe(target=text['remove_vk_describe_target'])
    async def remove_vk(self, interaction: discord.Interaction, target: discord.Member):
        await interaction.response.defer()

        data_base_connection = psycopg2.connect(
            host=config.db.host,
            port=config.db.port,
            database=config.db.name,
            user=config.db.user,
            password=config.db.password
        )
        data_base_cursor = data_base_connection.cursor()

        data_base_cursor.execute(f'DELETE FROM "Users" WHERE ds_id = {target.id} RETURNING ds_id, vk_id')
        data = data_base_cursor.fetchone()
        data_base_connection.commit()
        data_base_cursor.close()
        data_base_connection.close()

        if data:
            ds_id = data[0]
            vk_id = data[1]

            vk = vkbottle.API(config.vbot.token)
            vk_user = await vk.users.get(user_ids=data[1], name_case=text['vk_users_get_name_case'])
            vk_user = vk_user[0]

            try:
                await vk.messages.send(peer_id=vk_user.id,
                                       random_id=randint(0, 50000),
                                       message=text['remove_vk_direct_message'].format(ds_user_name=target.name))
            except VKAPIError[901]:
                pass

            embed = discord.Embed(
                title=text['remove_vk_embed_title'],
                description=text['remove_vk_embed_description'].format(
                    ds_user_name=target.mention,
                    vk_user_name=f'[{vk_user.first_name} {vk_user.last_name}](https://vk.com/id{vk_user.id})'
                ),
                colour=discord.Colour.green()
            )
            embed.set_image(url=text['remove_vk_embed_image'])

            await interaction.followup.send(embed=embed)

        else:
            embed = discord.Embed(
                title=text['remove_vk_embed_error_nothing_to_delete_title'],
                description=text['remove_vk_embed_error_nothing_to_delete_description'].format(
                    ds_user_name=target.name
                ),
                colour=discord.Colour.red()
            )
            embed.set_image(url=text['remove_vk_embed_error_nothing_to_delete_image'])

            await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RemoveVKCog(bot), guilds=[discord.Object(id=config.dbot.privileged_guild)])
