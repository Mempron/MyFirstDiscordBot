import discord

import traceback

from text import text


class MyTree(discord.app_commands.CommandTree):
    def __init__(self, bot):
        super().__init__(
            client=bot
        )

    async def on_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):

        if isinstance(error, discord.app_commands.errors.MissingAnyRole):
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=text['embed_error_missing_any_role_title'],
                description=text['embed_error_missing_any_role_description'].format(
                    ds_user_name=interaction.user.mention
                ),
            )

            embed.set_image(url=text['embed_error_missing_any_role_image'])
            await interaction.response.send_message(embed=embed)
            return

        traceback.print_exception(error)
