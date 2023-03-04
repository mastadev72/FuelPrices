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
    'type_alt': f'Fuel alternative type: {", ".join([i[0] for i in settings.FUEL_TYPES])}'
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
        fuel_types = [i[0] for i in settings.FUEL_TYPES]

        if type_alt not in fuel_types:
            api.abort(404, f"Fuel type '{type_alt}' not found. Available fuel types: {', '.join(fuel_types)}")

        fuel_prices = get_fuel_prices_by_type(type_alt).all()

        return fuel_prices
