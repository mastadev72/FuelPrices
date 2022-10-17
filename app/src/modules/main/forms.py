from flask_wtf import FlaskForm
from wtforms import SelectField

from src.settings import BaseConfig


class ComparePriceForm(FlaskForm):
    """index.html price comparison form."""

    type_alt = SelectField('საწვავის ტიპი', choices=BaseConfig.get_fuel_types())
