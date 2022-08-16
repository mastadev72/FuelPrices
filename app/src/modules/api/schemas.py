from marshmallow.fields import DateTime

from .api import ma
from src.modules.main.models import FuelPriceModel


class FuelPriceSchema(ma.SQLAlchemyAutoSchema):
    date = DateTime('%d-%m-%Y')
    last_updated = DateTime('%d-%m-%Y %H:%M:%S')

    class Meta:
        model = FuelPriceModel
        exclude = ('id',)
