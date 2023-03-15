from logging.config import dictConfig

from flask import Flask, render_template

from .database import db
from .settings import settings
from .extensions import extensions, extensions_with_db


def import_models() -> None:
    """Import models here for Flask-Migrate to work."""
    from src.modules.main.models import FuelPriceModel  # noqa: F401


def register_extensions(app: Flask) -> None:
    """Register Flask extensions."""
    for extension in extensions:
        extension.init_app(app=app)

    for extension in extensions_with_db:
        extension.init_app(app=app, db=db)


def register_blueprints(app: Flask) -> None:
    """
    Method to register list of blueprints to the app.

    :param app: Flask application
    :return: None
    """
    # To check if app contains blueprints we need to be inside the app context
    from src.utils.blueprints import blueprints

    if not blueprints and app.get("CHECK_FOR_BLUEPRINTS") is True:
        message = "The list of blueprints is empty. App won't have any blueprints."
        app.logger.warning(message)
    else:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)


def register_error_handlers(app: Flask) -> None:
    """Register error handlers here."""

    @app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        """404 error handler."""
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(*args, **kwargs):
        """500 error handler."""
        return render_template("500.html"), 500


def register_shell_context(app: Flask) -> None:
    """Register shell context here."""
    pass


def register_commands(app: Flask) -> None:
    """Register flask commands here."""
    from src.commands import fill_db
    app.cli.add_command(fill_db)


def register_formatters(app: Flask) -> None:
    """Register formatters here."""
    from src.formatters.dtime import datetimefilter
    app.jinja_env.filters["datetimefilter"] = datetimefilter


def configure_logger() -> None:
    """Configure logger here."""
    debug = settings.get_debug_status()

    dictConfig({
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
            "access": {
                "format": "%(message)s",
            }
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "slack": {
                "class": "src.error_handlers.HTTPSlackHandler",
                "formatter": "default",
                "level": "WARNING",
            },
        },
        "loggers": {
            "gunicorn.error": {
                "handlers": ["console"] if debug else ["console", "slack"],
                "level": "INFO",
                "propagate": False,
            },
            "gunicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            }
        },
        "root": {
            "level": "DEBUG" if debug else settings.get_log_level(),
            "handlers": ["console"] if debug else ["console", "slack"],
        }
    })


def create_app() -> Flask:
    """
    Create application factory.

    :return: Flask application
    """
    configure_logger()

    app = Flask(__name__)
    app.config.from_object(settings)

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)
    register_formatters(app)

    return app
