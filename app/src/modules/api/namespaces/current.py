from flask_restx import Resource, Namespace

from src.modules.main.models import FuelPriceModel

api = Namespace('Current Prices')


@api.route("/")
class Current(Resource):
    """All current prices API Current endpoint."""

    def get(self):
        """
        Get request method for API endpoint.

        :return: json with all current prices data
        """
        from src.modules.api.schemas import FuelPriceSchema

        fuel_objects = FuelPriceModel.read_current_prices()
        return FuelPriceSchema(many=True).dump(fuel_objects)


@api.route("/<string:provider>")
@api.response(404, 'Provider not found')
@api.doc(params={'provider': 'Provider name (gulf, wissol, rompetrol, socar, lukoil)'})
class ProviderCurrent(Resource):
    """Provider current prices API endpoint."""

    def get(self, provider):
        """
        Get request method for API ProviderCurrent endpoint.

        :param provider: fuel provider name
        :return: json with provider current prices data
        """
        from src.modules.api.schemas import FuelPriceSchema

        if provider.lower() not in ['gulf', 'wissol', 'rompetrol', 'socar', 'lukoil']:
            return 'Provider not found', 404

        fuel_objects = FuelPriceModel.read_current_prices(
            {
                'provider': provider.capitalize()
            }
        )
        return FuelPriceSchema(many=True).dump(fuel_objects)
