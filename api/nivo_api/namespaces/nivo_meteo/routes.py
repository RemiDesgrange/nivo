from uuid import UUID

from flask import jsonify
from flask_restx import Namespace, Resource, fields

from nivo_api.core.api_schema.geojson import Feature, FeatureCollection
from nivo_api.core.db.connection import connection_scope, session_scope
from nivo_api.core.db.models.orm.nivo import NivoRecord, SensorStation
from nivo_api.core.db.models.sql.nivo import SensorStationTable, NivoRecordTable
from nivo_api.namespaces.utils import UUIDField

nivo_meteo = Namespace("nivo-meteo", path="/nivo")
nivo_meteo.add_model("Feature", Feature)
nivo_meteo.add_model("FeatureCollection", FeatureCollection)


records_model = nivo_meteo.model(
    "RecordsModel",
    {
        "id": UUIDField(attribute="nr_id"),
        "date": fields.DateTime(attribute="nr_date"),
        "haut_sta": fields.Float(attribute="nr_haut_sta"),
        "dd": fields.Integer(attribute="nr_dd"),
        "ff": fields.Float(attribute="nr_ff"),
        "t": fields.Float(attribute="nr_t"),
        "td": fields.Float(attribute="nr_td"),
        "u": fields.Integer(attribute="nr_u"),
        "ww": fields.Integer(attribute="nr_ww"),
        "w1": fields.Integer(attribute="nr_w1"),
        "w2": fields.Integer(attribute="nr_w2"),
        "n": fields.Float(attribute="nr_n"),
        "nbas": fields.Integer(attribute="nr_nbas"),
        "hbas": fields.Integer(attribute="nr_hbas"),
        "cl": fields.Integer(attribute="nr_cl"),
        "cm": fields.Integer(attribute="nr_cm"),
        "ch": fields.Integer(attribute="nr_ch"),
        "rr24": fields.Float(attribute="nr_rr24"),
        "tn12": fields.Float(attribute="nr_tn12"),
        "tn24": fields.Float(attribute="nr_tn24"),
        "tx12": fields.Float(attribute="nr_tx12"),
        "tx24": fields.Float(attribute="nr_tx24"),
        "ht_neige": fields.Float(attribute="nr_ht_neige"),
        "ssfrai": fields.Float(attribute="nr_ssfrai"),
        "perssfrai": fields.Float(attribute="nr_perssfrai"),
        "phenspe1": fields.Float(attribute="nr_phenspe1"),
        "phenspe2": fields.Float(attribute="nr_phenspe2"),
        "nnuage1": fields.Integer(attribute="nr_nnuage1"),
        "t_neige": fields.Float(attribute="nr_t_neige"),
        "etat_neige": fields.Integer(attribute="nr_etat_neige"),
        "prof_sonde": fields.Integer(attribute="nr_prof_sonde"),
        "nuage_val": fields.Integer(attribute="nr_nuage_val"),
        "chasse_neige": fields.Integer(attribute="nr_chasse_neige"),
        "aval_descr": fields.Integer(attribute="nr_aval_descr"),
        "aval_genre": fields.Integer(attribute="nr_aval_genre"),
        "aval_depart": fields.Integer(attribute="nr_aval_depart"),
        "aval_expo": fields.Integer(attribute="nr_aval_expo"),
        "aval_risque": fields.Integer(attribute="nr_aval_risque"),
        "dd_alti": fields.Integer(attribute="nr_dd_alti"),
        "ff_alti": fields.Float(attribute="nr_ff_alti"),
        "ht_neige_alti": fields.Float(attribute="nr_ht_neige_alti"),
        "neige_fraiche": fields.Float(attribute="nr_neige_fraiche"),
        "teneur_eau": fields.Integer(attribute="nr_teneur_eau"),
        "grain_predom": fields.Integer(attribute="nr_grain_predom"),
        "grain_nombre": fields.Integer(attribute="nr_grain_nombre"),
        "grain_diametr": fields.Integer(attribute="nr_grain_diametr"),
        "homogeneite": fields.Integer(attribute="nr_homogeneite"),
        "m_vol_neige": fields.Float(attribute="nr_m_vol_neige"),
    },
)


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
    def get(self, station_id: UUID):
        with session_scope() as sess:
            return (
                sess.query(NivoRecord)
                .join(SensorStation)
                .filter(SensorStation.nss_id == station_id)
                .all()
            )


@nivo_meteo.route("/stations/<uuid:station_id>/records/last")
class NivoRecordsBySensorStationResource(Resource):
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
                .first
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
