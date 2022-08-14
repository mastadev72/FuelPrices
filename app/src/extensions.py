# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_static_digest import FlaskStaticDigest
from flask_mail import Mail
from flask_restx import Api

from src.database import db

api = Api(
	doc="/api", prefix="/api", title="Fuel Prices API"
)
migrate = Migrate()
mail = Mail()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()

extensions = [db, api, mail, cache, debug_toolbar, flask_static_digest]
extensions_with_db = [migrate]
