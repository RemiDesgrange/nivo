from uuid import UUID

from flask import jsonify
from flask_restplus import Namespace, Resource

from nivo_api.core.api_schema.geojson import Feature, FeatureCollection
from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.nivo import NivoSensorStation, NivoRecord

nivo_meteo = Namespace('nivo-meteo', path='/nivo')
nivo_meteo.add_model('Feature', Feature)
nivo_meteo.add_model('FeatureCollection', FeatureCollection)

@nivo_meteo.route('/stations')
class NivoSensorStationResource(Resource):
    @nivo_meteo.response(200, 'OK', FeatureCollection)
    def get(self):
        with connection_scope() as con:
            res = NivoSensorStation.get_geojson(con)
        return jsonify(res)


@nivo_meteo.route('/stations/<uuid:station_id>')
class OneNivoSensorStationResource(Resource):
    @nivo_meteo.response(200, 'OK', Feature)
    @nivo_meteo.response(404, "Not Found")
    def get(self, station_id: UUID):
        with connection_scope() as con:
            res = NivoSensorStation.get_geojson(con, station_id)
        return jsonify(res)


@nivo_meteo.route('/records')
class NivoRecordResource(Resource):
    @nivo_meteo.response(200, 'OK')
    def get(self):
        #TODO need limits
        with connection_scope() as con:
            res = NivoRecord.get_json(con)
        return jsonify(res)


@nivo_meteo.route('/records/<uuid:record_id>')
class OneNivoRecordResource(Resource):
    @nivo_meteo.response(200, 'OK')
    @nivo_meteo.response(404, 'Not Found')
    def get(self, record_id: UUID):
        with connection_scope() as con:
            res = NivoRecord.get_json(con, record_id)
        return jsonify(res)


@nivo_meteo.route('/records/<date:date_from>/<date:date_to>')
class NivoRecordDateResource(Resource):
    @nivo_meteo.response(200, 'OK')
    def get(self, date_from, date_to):
        raise NotImplemented()

