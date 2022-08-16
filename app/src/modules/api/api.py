from flask import Blueprint
from flask_restx import Api
from flask_marshmallow import Marshmallow

from .namespaces.current import api as current_ns


api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_blueprint, title="Fuel Prices API", version='1.0')
ma = Marshmallow()

api.add_namespace(current_ns, path='/current')
