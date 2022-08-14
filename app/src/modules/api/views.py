from flask_restx import Resource

from src.extensions import api


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
