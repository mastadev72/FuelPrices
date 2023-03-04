from flask_restx import Resource, Namespace, fields

from src.extensions import cache
from src.settings import settings

api = Namespace('Utilities')

fuel_types_sr = api.model('FuelTypes', {
    'name': fields.String(required=True, description="Fuel name"),
    'type_alt': fields.String(required=True, description="Fuel alternative name"),
})


@api.route("/fuel-types")
class FuelTypes(Resource):
    """All fuel types API endpoint."""

    @api.doc('get_all_fuel_types')
    @api.marshal_list_with(fuel_types_sr)
    @cache.cached(timeout=10*60)
    def get(self):
        """
        Get all fuel types.

        :return: json with all fuel types
        """
        fuel_types = []

        for obj in settings.FUEL_TYPES:
            fuel_types.append({
                "name": obj[1],
                "type_alt": obj[0]
            })

        return fuel_types
