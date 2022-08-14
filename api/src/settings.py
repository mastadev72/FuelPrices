# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set environment variables.
"""
from environs import Env

env = Env()
env.read_env()


class Config(object):
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
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
