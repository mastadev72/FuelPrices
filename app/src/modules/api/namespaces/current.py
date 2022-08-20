from flask_restx import Resource, Namespace

from src.modules.main.models import FuelPriceModel

api = Namespace('Current Prices')


@api.route("/")
class Current(Resource):
    def get(self):
        from src.modules.api.schemas import FuelPriceSchema

        fuel_objects = FuelPriceModel.read_current_prices()
        return FuelPriceSchema(many=True).dump(fuel_objects)


@api.route("/<string:provider>")
@api.response(404, 'Provider not found')
@api.doc(params={'provider': 'Provider name (gulf, wissol, rompetrol, socar, lukoil)'})
class Current(Resource):
    def get(self, provider):
        from src.modules.api.schemas import FuelPriceSchema

        if provider.lower() not in ['gulf', 'wissol', 'rompetrol', 'socar', 'lukoil']:
            return 'Provider not found', 404

        fuel_objects = FuelPriceModel.read_current_prices(provider=provider.capitalize())
        return FuelPriceSchema(many=True).dump(fuel_objects)


