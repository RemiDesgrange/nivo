from datetime import timedelta
from uuid import UUID

from flask import jsonify
from flask_restx import Resource
from sqlalchemy import func

from nivo_api.core.api_schema.geojson import Feature, FeatureCollection
from nivo_api.core.db.connection import connection_scope, session_scope
from nivo_api.core.db.models.orm.nivo import NivoRecord, SensorStation
from nivo_api.core.db.models.sql.nivo import SensorStationTable, NivoRecordTable
from .models import records_model, record_limit_parser

from .namespace import nivo_meteo


@nivo_meteo.route("/stations")
class NivoSensorStationResource(Resource):
    @nivo_meteo.response(200, "OK", FeatureCollection)
    def get(self):
        with connection_scope() as con:
            res = SensorStationTable.get_geojson(con)
        return jsonify(res)


@nivo_meteo.route("/stations/<uuid:station_id>")
class OneNivoSensorStationResource(Resource):
    @nivo_meteo.response(200, "OK", Feature)
    @nivo_meteo.response(404, "Not Found")
    def get(self, station_id: UUID):
        with connection_scope() as con:
            res = SensorStationTable.get_geojson(con, station_id)
        return jsonify(res)


@nivo_meteo.route("/stations/<uuid:station_id>/records")
class NivoRecordsBySensorStationResource(Resource):
    @nivo_meteo.response(200, "OK", records_model)
    @nivo_meteo.response(404, "Not Found")
    @nivo_meteo.marshal_with(records_model)
    @nivo_meteo.expect(record_limit_parser)
    def get(self, station_id: UUID):
        args = record_limit_parser.parse_args()
        with session_scope() as sess:
            limit = args.get("limit", None)
            limit_by_day = args.get("day_limit", None)

            req = (
                sess.query(NivoRecord)
                .filter(NivoRecord.nr_nivo_sensor == station_id)
                .order_by(NivoRecord.nr_date.desc())
            )
            if limit_by_day:
                last_date = sess.query(func.max(NivoRecord.nr_date).label('max')).filter(NivoRecord.nr_nivo_sensor == station_id).subquery('last_date')
                req = req.filter(func.age(last_date.c.max, NivoRecord.nr_date) < timedelta(days=limit_by_day))
            if limit:
                req = req.limit(limit)
            return req.all()


@nivo_meteo.route("/stations/<uuid:station_id>/records/last")
class LastNivoRecordsBySensorStationResource(Resource):
    @nivo_meteo.response(200, "OK", records_model)
    @nivo_meteo.response(404, "Not Found")
    @nivo_meteo.marshal_with(records_model)
    def get(self, station_id: UUID):
        with session_scope() as sess:
            return (
                sess.query(NivoRecord)
                .join(SensorStation)
                .filter(SensorStation.nss_id == station_id)
                .order_by(NivoRecord.nr_date.desc())
                .limit(1)
                .first()
            )


@nivo_meteo.route("/records/<uuid:record_id>")
class OneNivoRecordResource(Resource):
    @nivo_meteo.response(200, "OK", records_model)
    @nivo_meteo.response(404, "Not Found")
    @nivo_meteo.marshal_with(records_model)
    def get(self, record_id: UUID):
        with connection_scope() as con:
            res = NivoRecordTable.get_json(con, record_id)
        return res


@nivo_meteo.route("/records/<string:date_from>/<string:date_to>")
class NivoRecordDateResource(Resource):
    @nivo_meteo.response(200, "OK")
    def get(self, date_from, date_to):
        raise NotImplementedError()
