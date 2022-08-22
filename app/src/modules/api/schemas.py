from marshmallow.fields import DateTime

from src.modules.api.api import ma
from src.modules.main.models import FuelPriceModel


class FuelPriceSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """Schema for FuelPriceModel."""

    date = DateTime('%d-%m-%Y')
    last_updated = DateTime('%d-%m-%Y %H:%M:%S')

    class Meta:  # noqa: D106
        model = FuelPriceModel
        exclude = ('id',)
