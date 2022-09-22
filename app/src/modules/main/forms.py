from flask_wtf import FlaskForm
from wtforms import SelectField

from src.settings import Config


class ComparePriceForm(FlaskForm):
    """index.html price comparison form."""

    type_alt = SelectField('საწვავის ტიპი', choices=Config.get_fuel_types())
