from flask import Blueprint
from flask_restx import Api
from flask_marshmallow import Marshmallow

from .namespaces.current import api as current_ns
from .namespaces.best_deals import api as lowest_deals_ns
from .namespaces.utils import api as utils_ns
from .namespaces.compare import api as compare_ns

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_blueprint, title="Fuel Prices API", version='1.0')
ma = Marshmallow()

# TODO: Add missing api tests + add unit tests

api.add_namespace(current_ns, path='/current')
api.add_namespace(lowest_deals_ns, path='/lowest')
api.add_namespace(compare_ns, path='/compare')
api.add_namespace(utils_ns, path='/utils')
