import discord
from discord import app_commands
from discord.ext import commands
from vkbottle import VKAPIError

from random import randint

from config import config, database, api


class RemoveVKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='remove_vk', description=config.text['remove_vk_description'])
    @app_commands.guilds(config.discord_bot.privileged_guild)
    @app_commands.checks.has_any_role(*config.discord_bot.privileged_roles)
    @app_commands.describe(target=config.text['remove_vk_describe_target'])
    async def remove_vk(self, interaction: discord.Interaction, target: discord.Member):
        cursor = database.cursor()
        cursor.execute(f'SELECT * FROM "Users" WHERE ds_id = {target.id}')
        data = cursor.fetchone()
        if data:
            vk_user = await api.users.get(user_ids=data[1], name_case=config.text['vk_users_get_name_case'])
            vk_user = vk_user[0]

            try:
                await api.messages.send(peer_id=vk_user.id,
                                        random_id=randint(0, 50000),
                                        message=config.text['remove_vk_direct_message'].format(
                                            ds_user_name=target.name
                                        ))
            except VKAPIError[901]:
                pass

            cursor.execute(f'DELETE FROM "Users" WHERE ds_id = {target.id}')
            database.commit()

            embed = discord.Embed(
                title=config.text['remove_vk_embed_title'],
                description=config.text['remove_vk_embed_description'].format(
                    ds_user_name=target.mention,
                    vk_user_name=f'[{vk_user.first_name} {vk_user.last_name}](https://vk.com/id{vk_user.id})'
                ),
                colour=discord.Colour.green()
            )
            embed.set_image(url=config.text['remove_vk_embed_image'])

            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title=config.text['remove_vk_embed_error_nothing_to_delete_title'],
                description=config.text['remove_vk_embed_error_nothing_to_delete_description'].format(
                    ds_user_name=target.name
                ),
                colour=discord.Colour.red()
            )
            embed.set_image(url=config.text['remove_vk_embed_error_nothing_to_delete_image'])

            await interaction.response.send_message(embed=embed)

    @remove_vk.error
    async def remove_vk_error(self, interaction: discord.Interaction, error):
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
    await bot.add_cog(RemoveVKCog(bot), guilds=[discord.Object(id=config.discord_bot.privileged_guild)])
