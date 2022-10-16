# -*- coding: utf-8 -*-

import os
from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent

env = Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

bind = "0.0.0.0:" + env.str("PORT")
workers = env.int("GUNICORN_WORKERS")
worker_class = "gevent"
timeout = 300
max_requests = 1000000
limit_request_line = 8190

accesslog = "-"
errorlog = "-"
