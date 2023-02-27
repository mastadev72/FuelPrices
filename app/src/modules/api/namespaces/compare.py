from flask_restx import Resource, Namespace, fields

from src.settings import settings
from src.modules.main.services import get_fuel_prices_by_type

api = Namespace('Compare Prices')

compare_sr = api.model('FuelTypes', {
    'provider': fields.String(required=True, description="Fuel provider"),
    'price': fields.Float(required=True, description="Fuel price")
})


@api.route("/<string:type_alt>")
@api.doc(params={
    'type_alt': 'Fuel alternative type (diesel, regular, diesel_alt, regular_alt, premium_alt, super_alt)'
})
class Compare(Resource):
    """Compare fuel type prices API endpoint."""

    @api.doc('get_fuel_type_prices')
    @api.marshal_list_with(compare_sr)
    def get(self, type_alt):
        """
        Get fuel type prices.

        :return: json with all fuel type prices
        """
        fuel_alt_types = [i[0] for i in settings.FUEL_TYPES]

        if type_alt not in fuel_alt_types:
            api.abort(404, f"Fuel type '{type_alt}' not found. Available fuel types: {fuel_alt_types}")

        fuel_prices = get_fuel_prices_by_type(type_alt).all()

        return fuel_prices
