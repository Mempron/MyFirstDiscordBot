import psycopg2
import vkbottle
from environs import Env

from dataclasses import dataclass

from texts import text


@dataclass
class DiscordBot:
    token: str
    vac_role: int
    vac_channel: int
    privileged_roles: list[int]
    privileged_guild: int
    application_id: int
    cogs: list[str]


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
    text: dict


env = Env()
env.read_env()

config = Config(
    discord_bot=DiscordBot(
        token=env.str('DISCORD_BOT_TOKEN'),
        vac_role=env.int('DISCORD_BOT_VAC_ROLE'),
        vac_channel=env.int('DISCORD_BOT_VAC_CHANNEL'),
        privileged_roles=env.list('DISCORD_BOT_PRIVILEGED_ROLES', subcast=int),
        privileged_guild=env.int('DISCORD_BOT_PRIVILEGED_GUILD'),
        application_id=env.int('DISCORD_APPLICATION_ID'),
        cogs=[
            'help',
            'ping',
            'add_vk',
            'remove_vk',
            'list_vk',
            'vac',
            'list_vac',
            'cancel_vac',
            'remind',
            'list_reminds',
            'cancel_remind',
        ]
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
    ),
    text=text
)
database = psycopg2.connect(
    host=config.data_base.host,
    port=config.data_base.port,
    database=config.data_base.name,
    user=config.data_base.user,
    password=config.data_base.password
)
api = vkbottle.API(config.vk_bot.token)
