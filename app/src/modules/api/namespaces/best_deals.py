from flask_restx import Resource, Namespace, fields

from src.extensions import cache
from src.modules.main.services import get_lowest_current_prices

api = Namespace('Lowest Deals')

lowest_sr = api.model('Lowest', {
    'fuel_type': fields.String(required=True, description="Fuel type"),
    'price': fields.Float(required=True, description="Fuel price"),
    'providers': fields.List(fields.String, required=True, description="Fuel Providers")
})


@api.route("/")
class Lowest(Resource):
    """All lowest prices API endpoint."""

    @api.doc('get_lowest_prices')
    @api.marshal_with(lowest_sr)
    @cache.cached(timeout=3 * 60)
    def get(self):
        """
        Get lowest prices for each fuel type.

        :return: json with all lowest prices data
        """
        fuel_objects = []
        lowest_prices = get_lowest_current_prices()

        for obj in lowest_prices:
            fuel_objects.append({
                'fuel_type': obj[0],
                'price': obj[1][1],
                'providers': obj[1][0]
            })

        return fuel_objects
