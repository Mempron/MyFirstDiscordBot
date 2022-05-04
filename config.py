from environs import Env

from dataclasses import dataclass


@dataclass
class DiscordBot:
    token: str
    vac_role: int
    vac_channel: int
    privileged_roles: list[str]
    privileged_guild: int


@dataclass
class VKBot:
    token: str


@dataclass
class DataBase:
    host: str
    port: str
    name: str
    user: str
    password: str


@dataclass
class Config:
    discord_bot: DiscordBot
    vk_bot: VKBot
    data_base: DataBase


def get_config():
    env = Env()
    env.read_env()

    return Config(
        discord_bot=DiscordBot(
            token=env.str('DISCORD_BOT_TOKEN'),
            vac_role=env.int('DISCORD_BOT_VAC_ROLE'),
            vac_channel=env.int('DISCORD_BOT_VAC_CHANNEL'),
            privileged_roles=env.list('DISCORD_BOT_PRIVILEGED_ROLES'),
            privileged_guild=env.int('DISCORD_BOT_PRIVILEGED_GUILD')
        ),
        vk_bot=VKBot(
            token=env.str('VK_BOT_TOKEN')
        ),
        data_base=DataBase(
            host=env.str('DATABASE_HOST'),
            port=env.str('DATABASE_PORT'),
            name=env.str('DATABASE_NAME'),
            user=env.str('DATABASE_USER'),
            password=env.str('DATABASE_PASSWORD')
        )
    )
