from flask_wtf import FlaskForm
from wtforms import SelectField

FUEL_TYPES = (
    ('diesel', "ევრო დიზელი"),
    ('regular', "ევრო რეგულარი"),
    ('diesel_alt', "დიზელი"),
    ('regular_alt', "რეგულარი"),
    ('premium_alt', "პრემიუმი"),
    ('super_alt', "სუპერი")
)


class ComparePriceForm(FlaskForm):
    type_alt = SelectField('საწვავის ტიპი', choices=FUEL_TYPES)
