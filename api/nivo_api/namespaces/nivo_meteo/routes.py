import json
from uuid import UUID

from flask_restplus import Namespace, Resource

from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.nivo import NivoSensorStation

nivo_meteo = Namespace('nivo-meteo', path='/nivo')

@nivo_meteo.route('/stations')
@nivo_meteo.route('/stations/<uuid:station_id>')
class NivoSensorStationResource(Resource):

    def get(self, station_id: UUID = None):
        with connection_scope() as con:
            res = NivoSensorStation.get_geojson(con, station_id)
        return str(res)