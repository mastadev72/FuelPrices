# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_static_digest import FlaskStaticDigest
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.database import db

migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()
limiter = Limiter(
    get_remote_address,
    strategy="fixed-window"
)

extensions = [db, cache, debug_toolbar, flask_static_digest, limiter]
extensions_with_db = [migrate]
