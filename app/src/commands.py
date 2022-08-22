import click
from flask.cli import with_appcontext

from src.modules.crontab.main import parse_data


@click.command('fill_db')
@with_appcontext
def fill_db():  # noqa: D103
    parse_data()
