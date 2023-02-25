from flask_restx import Resource, Namespace, fields

from src.modules.main.models import FuelPriceModel
from src.settings import settings

api = Namespace('Current Prices')

fuel_sr = api.model('Fuel', {
    'name': fields.String(required=True, description="Fuel name"),
    'type_alt': fields.String(required=True, description="Fuel alternative name"),
    'price': fields.Float(required=True, description="Fuel price"),
    'change_rate': fields.Float(required=True, description="Fuel price change rate"),
    'date': fields.DateTime(required=True, description="Fuel price date"),
    'last_updated': fields.DateTime(required=True, description="Fuel price last updated"),
})

current_sr = api.model('Current', {
    'provider': fields.String(required=True, description='Provider name'),
    'last_updated': fields.String(required=True, description="Fuel price last updated"),
    'fuel': fields.List(
        fields.Nested(fuel_sr)
    )
})


@api.route("/")
class Current(Resource):
    """All current prices API endpoint."""

    @api.doc('get_all_current_prices')
    @api.marshal_list_with(current_sr)
    def get(self):
        """
        Get all current prices.

        :return: json with all current prices data
        """
        providers = settings.FUEL_PROVIDERS
        objs = FuelPriceModel.read_current_prices().all()

        # Format last updated date
        last_updated = objs[0].last_updated.strftime('%H:%M %d-%b-%Y')

        data = []

        for provider in providers:
            data.append({
                'provider': provider,
                'last_updated': last_updated,
                'fuel': [i for i in objs if i.provider == provider]
            })

        return data


@api.route("/<string:provider>")
@api.response(404, 'Provider not found')
@api.doc(params={'provider': 'Provider name (gulf, wissol, rompetrol, socar, lukoil)'})
class ProviderCurrent(Resource):
    """Provider current prices API endpoint."""

    @api.doc('get_provider_current_prices')
    @api.marshal_list_with(current_sr)
    def get(self, provider):
        """
        Get all provider prices.

        :param provider: fuel provider name
        :return: json with provider current prices data
        """
        if provider.lower() not in ['gulf', 'wissol', 'rompetrol', 'socar', 'lukoil']:
            return 'Invalid provider name.', 409

        fuel_objects = FuelPriceModel.read_current_prices(
            {
                'provider': provider.capitalize()
            }
        ).all()

        # Format last updated date
        last_updated = fuel_objects[0].last_updated.strftime('%H:%M %d-%b-%Y')

        data = {
            'provider': provider.capitalize(),
            'last_updated': last_updated,
            'fuel': [i for i in fuel_objects]
        }

        return data
