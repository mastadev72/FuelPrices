# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set environment variables.
"""
import os
from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

env = Env()
env.read_env(os.path.join(BASE_DIR, 'envs/.env.dev'))


class BaseConfig(object):
    """Config class for flask application."""

    # Flask
    ENV = env.str("FLASK_ENV", default="production")
    DEBUG = ENV == "development"
    SECRET_KEY = env.str("SECRET_KEY")
    LOG_LEVEL = env.str("LOG_LEVEL", default="INFO")
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Static
    STATIC_FOLDER = os.path.join(SRC_DIR, 'static')

    # Database
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cache
    CACHE_TYPE = env.str("CACHE_TYPE")

    # API
    JSON_SORT_KEYS = False

    # Slack logger
    SLACK_WEBHOOK_KEY = env.str("SLACK_WEBHOOK_KEY")

    # App specific
    FUEL_TYPES = (
        ('diesel', "ევრო დიზელი"),
        ('regular', "ევრო რეგულარი"),
        ('diesel_alt', "დიზელი"),
        ('regular_alt', "რეგულარი"),
        ('premium_alt', "პრემიუმი"),
        ('super_alt', "სუპერი")
    )

    CHART_TOTAL_DAYS = 10  # Analytics chart total display days

    @classmethod
    def get_debug_status(cls) -> bool:
        """Get DEBUG status."""
        return cls.DEBUG

    @classmethod
    def get_slack_webhook_key(cls) -> str:
        """Get slack webhook key."""
        return cls.SLACK_WEBHOOK_KEY

    @classmethod
    def get_fuel_types(cls) -> tuple:
        """Get supported fuel types."""
        return cls.FUEL_TYPES

    @classmethod
    def get_chart_total_days(cls) -> int:
        """Get total days for analytics chart to display."""
        return cls.CHART_TOTAL_DAYS

    @classmethod
    def get_static_folder(cls) -> str:
        """Get total days for analytics chart to display."""
        return cls.STATIC_FOLDER

    @classmethod
    def get_log_level(cls) -> str:
        """Get log level."""
        return cls.LOG_LEVEL


class Production(BaseConfig):
    """Production configuration."""

    DEBUG = False

    # Database
    db_user = env.str("DATABASE_USERNAME", default="postgres")
    db_pass = env.str("DATABASE_PASSWORD", default="postgres")
    db_host = env.str("DATABASE_HOST", default="localhost")
    db_port = env.str("DATABASE_PORT", default="5432")
    db_name = env.str("DATABASE_NAME", default="postgres")

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://' \
                              f'{db_user}:{db_pass}@' \
                              f'{db_host}:{db_port}/{db_name}'

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_reset_on_return": 'commit',  # looks like postgres likes this more than rollback
        'pool_size': env.int("SQLALCHEMY_POOL_SIZE", default=20),
        'pool_recycle': env.int("SQLALCHEMY_POOL_RECYCLE", default=1200),
        'pool_timeout': env.int("SQLALCHEMY_POOL_TIMEOUT", default=5),
        'max_overflow': env.int("SQLALCHEMY_MAX_OVERFLOW", default=10),
    }

    # Cache
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://redis:6379/0"
    CACHE_DEFAULT_TIMEOUT = 500
