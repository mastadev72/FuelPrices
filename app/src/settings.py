# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set environment variables.
"""
from environs import Env

env = Env()
env.read_env()


class Config(object):
    """Config class for flask application."""

    # Flask
    ENV = env.str("FLASK_ENV", default="production")
    DEBUG = ENV == "development"
    SECRET_KEY = env.str("SECRET_KEY")
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Database
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cache
    CACHE_TYPE = env.str("CACHE_TYPE")
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://redis:6379/0"
    CACHE_DEFAULT_TIMEOUT = 500

    # API
    JSON_SORT_KEYS = False

    # Slack logger
    SLACK_WEBHOOK_KEY = env.str("SLACK_WEBHOOK_KEY")

    @staticmethod
    def get_debug_status() -> bool:
        """Get DEBUG status."""
        return Config.DEBUG

    @staticmethod
    def get_slack_webhook_key() -> str:
        """Get slack webhook key."""
        return Config.SLACK_WEBHOOK_KEY
