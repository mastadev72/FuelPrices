from flask import Flask

from .database import db
from .settings import Config
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
    from .utils import blueprints

    if not blueprints and app.get("CHECK_FOR_BLUEPRINTS") is True:
        message = "The list of blueprints is empty. App won't have any blueprints."
        app.logger.warning(message)
    else:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)


def register_error_handlers(app: Flask) -> None:
    """Register error handlers here."""
    from src.errors import page_not_found

    app.register_error_handler(404, page_not_found)


def register_shell_context(app: Flask) -> None:
    """Register shell context here."""
    pass


def register_commands(app: Flask) -> None:
    """Register flask commands here."""
    from src.commands import fill_db
    app.cli.add_command(fill_db)


def configure_logger(app: Flask) -> None:
    """Configure logger here."""
    pass


def create_app() -> Flask:
    """
    Create application factory.

    :return: Flask application
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["DEBUG"] = True

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)
    configure_logger(app)

    return app