import logging
import os
from dataclasses import dataclass
from logging import getLogger
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

BOT_TOKEN_ENV = "BOT_TOKEN"
BOT_ADMIN_IDS_ENV = "BOT_ADMIN_IDS"

DB_USER_ENV = "DB_USER"
DB_PASSWORD_ENV = "DB_PASSWORD"
DB_HOST_ENV = "DB_HOST_ENV"
DB_NAME_ENV = "DB_NAME_ENV"
DB_PORT_ENV = "DB_PORT"

REDIS_HOST = "REDIS_HOST"
REDIS_PORT = "REDIS_PORT"
REDIS_DB = "REDIS_DB"
REDIS_MAX_CONNECTION = "REDIS_MAX_CONNECTION"

RAPID_API_KEY = "RAPID_API_KEY"
RAPID_API_HOST = "RAPID_API_HOST"

FILE_SIZE_LIMIT = "FILE_SIZE_LIMIT"
FILE_DURATION_LIMIT = "FILE_DURATION_LIMIT"

logger = getLogger(__name__)
load_dotenv()

class ConfigParseError(ValueError):
    pass

@dataclass
class RapidApiConfig:
    rapid_api_key: str
    rapid_api_host: str

@dataclass
class BotConfig:
    bot_token: str
    admin_ids: int

@dataclass
class RedisConfig:
    redis_host: str
    redis_port: int
    redis_db: int
    redis_max_connection: int

@dataclass
class DatabaseConfig:
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    db_port: str

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

@dataclass
class ApplicationSettingsConfig:
    file_size_limit: float
    file_duration_limit: float


def get_str_env(key) -> str:
    val = os.getenv(key)

    if not val:
        logger.error("%s is not set", key)
        raise ConfigParseError(f"{key} is not set")

    return val

def load_bot_config() -> BotConfig:
    logger.info("Reading bot config from .env file")

    bot_token = get_str_env(BOT_TOKEN_ENV)
    admin_ids = get_str_env(BOT_ADMIN_IDS_ENV)

    return BotConfig(
        bot_token=bot_token,
        admin_ids=int(admin_ids)
    )

def load_rapid_api_config() -> RapidApiConfig:
    logger.info("Reading rapid api config from .env file")

    rapid_api_key = get_str_env(RAPID_API_KEY)
    rapid_api_host = get_str_env(RAPID_API_HOST)

    return RapidApiConfig(
        rapid_api_key=rapid_api_key,
        rapid_api_host=rapid_api_host
    )

def load_database_config() -> DatabaseConfig:
    db_user = get_str_env(DB_USER_ENV)
    db_password = get_str_env(DB_PASSWORD_ENV)
    db_host = get_str_env(DB_HOST_ENV)
    db_name = get_str_env(DB_NAME_ENV)
    db_port = get_str_env(DB_PORT_ENV)

    return DatabaseConfig(
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_name=db_name,
        db_port=db_port
    )

def load_redis_config() -> RedisConfig:
    redis_host = get_str_env(REDIS_HOST)
    redis_port = int(get_str_env(REDIS_PORT))
    redis_db = int(get_str_env(REDIS_DB))
    redis_max_connection = int(get_str_env(REDIS_MAX_CONNECTION))

    return RedisConfig(
        redis_host=redis_host,
        redis_port=redis_port,
        redis_db=redis_db,
        redis_max_connection=redis_max_connection
    )

def load_application_specific_config() -> ApplicationSettingsConfig:
    file_size_limit = float(get_str_env(FILE_SIZE_LIMIT))
    file_duration_limit = float(get_str_env(FILE_DURATION_LIMIT))

    return ApplicationSettingsConfig(
        file_size_limit=file_size_limit,
        file_duration_limit=file_duration_limit
    )

bot_config = load_bot_config()

bot = Bot(token=bot_config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
admins = bot_config.admin_ids

logging.basicConfig(level=logging.INFO)