import discord

import typing

from config import config
from text import text


async def get_targets(interaction: discord.Interaction, unknown_targets: typing.Union[discord.Role, discord.Member]):
    vacationers = []
    targets = []

    if isinstance(unknown_targets, discord.role.Role):
        for member in unknown_targets.members:
            vacation = discord.utils.get(member.roles, id=config.dbot.vac_role)
            if vacation:
                vacationers.append(member)
        targets = list(set(unknown_targets.members) - set(vacationers))
    elif isinstance(unknown_targets, discord.Member):
        vacation = discord.utils.get(unknown_targets.roles, id=config.dbot.vac_role)
        if vacation:
            vacationers.append(unknown_targets)
        else:
            targets.append(unknown_targets)
    if vacationers:
        if interaction.command.name == 'cancel_vac':
            return targets, vacationers

        ds_users_names = ', '.join([vacationer.mention for vacationer in vacationers])

        if interaction.command.name == 'vac':
            embed = discord.Embed(
                title=text['vac_embed_error_vac_already_title'],
                description=text['vac_embed_vac_already_description'].format(
                    ds_users_names=ds_users_names
                ),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=text['vac_embed_vac_already_image'])
        else:
            embed = discord.Embed(
                title=text['vacation_error_embed_title'],
                description=text['vacation_error_embed_description'].format(ds_users_names=ds_users_names),
                colour=discord.Colour.orange()
            )
            embed.set_image(url=text['vacation_error_embed_image'])

        await interaction.followup.send(embed=embed)

    return targets
