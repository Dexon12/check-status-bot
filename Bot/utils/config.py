"""this module consists of configuration classes"""
import os

from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class DbConfig:
    password: str
    user: str
    database: str
    host: str = field(default='localhost')


@dataclass
class TgBot:
    token: str 
    admin_id: str
    redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str = None) -> Config:
    load_dotenv(path)  # loading the necessary .envs when the main process os initialized

    return Config(
        tg_bot=TgBot(
            token=os.getenv('TOKEN_API'),
            admin_id=os.getenv('ADMINS'),
            redis=False  # if True - we use redis else - False
        ),
        db=DbConfig(
            host=os.getenv('DB_HOST'),
            password=os.getenv('DB_PASSWORD'),
            user=os.getenv('DB_USER'),
            database=os.getenv('DB_NAME')
        )
    )
