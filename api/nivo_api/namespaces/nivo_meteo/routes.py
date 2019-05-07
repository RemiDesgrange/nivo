from flask_restplus import Namespace, Resource

nivo_meteo = Namespace('nivo-meteo')


@nivo_meteo.route('/')
class NivoMeteo(Resource):

    def get(self, date=None):
        return ''