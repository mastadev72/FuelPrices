from flask_wtf import FlaskForm
from wtforms import SelectField

from src.settings import settings


class ComparePriceForm(FlaskForm):
    """index.html price comparison form."""

    type_alt = SelectField('საწვავის ტიპი', choices=settings.get_fuel_types())
