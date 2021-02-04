from typing import Optional, Dict, List, Union
from uuid import UUID

from flask import jsonify
from flask_restx import Resource, marshal
from flask_restx._http import HTTPStatus
from geojson import FeatureCollection, Feature
from sqlalchemy import select, Date, func, true
from sqlalchemy.orm import subqueryload
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql.functions import concat

from nivo_api.core.api_schema.geojson import (
    FeatureCollection as FeatureCollectionSchema,
)
from nivo_api.core.db.connection import connection_scope, session_scope
from nivo_api.core.db.models.orm.bra import Massif, Department, Zone, BraRecord
from nivo_api.core.db.models.sql.bra import (
    DepartmentTable,
    BraRecordTable,
    MassifTable,
    RiskTable,
)
from nivo_api.namespaces.bra.models import bra_model, zone_model, department_model, massifs_model
from nivo_api.namespaces.bra.namespace import bra_api
from nivo_api.namespaces.utils import GeometryField

massif_record_parser = bra_api.parser()
massif_record_parser.add_argument("limit", type=int, required=False, default=50)


@bra_api.route("/massifs/<uuid:massif_id>/records")
class MassifsRecordRessource(Resource):
    @bra_api.expect(massif_record_parser)
    def get(self, massif_id: UUID) -> List[Dict]:
        """
        Return a list of records for a massif. Limit to last 50 days by default.
        """
        args = massif_record_parser.parse_args()
        with session_scope() as sess:
            res = (
                sess.query(BraRecord)
                .filter(BraRecord.br_massif == massif_id)
                .filter(BraRecord.br_production_date > (func.now() - func.cast(concat(args["limit"], 'DAYS'), INTERVAL)))
                .order_by(BraRecord.br_production_date.desc())
                .options(subqueryload(BraRecord.risks))
                .options(subqueryload(BraRecord.snow_records))
                .options(subqueryload(BraRecord.fresh_snow_records))
                .options(subqueryload(BraRecord.weather_forcasts))
                .options(subqueryload(BraRecord.risk_forcasts))
                .options(subqueryload(BraRecord.massif))
                .all()
            )
            return marshal(res, bra_model)


@bra_api.route("/last")
class LastBraListResource(Resource):
    def get(self) -> Dict:
        """
        Return the last record for all massifs.
        """
        with session_scope() as sess:
            res = (
                sess.query(BraRecord)
                .join(Massif)
                .filter(
                    BraRecord.br_production_date.cast(Date)
                    == select([func.max(BraRecord.br_production_date.cast(Date))])
                )
                .options(subqueryload(BraRecord.risks))
                .options(subqueryload(BraRecord.snow_records))
                .options(subqueryload(BraRecord.fresh_snow_records))
                .options(subqueryload(BraRecord.weather_forcasts))
                .options(subqueryload(BraRecord.risk_forcasts))
                .all()
            )
            return marshal(res, bra_model)


@bra_api.route("/massifs/<uuid:massif_id>/last")
class LastBraRecordResource(Resource):
    def get(self, massif_id: UUID) -> Dict:
        """
        Return a record for a massifs. With all the associated metadata.
        """
        with session_scope() as sess:
            s = (
                sess.query(BraRecord)
                .filter(BraRecord.br_massif == massif_id)
                .order_by(BraRecord.br_production_date.desc())
                .limit(1)
                .options(subqueryload(BraRecord.risks))
                .options(subqueryload(BraRecord.snow_records))
                .options(subqueryload(BraRecord.fresh_snow_records))
                .options(subqueryload(BraRecord.weather_forcasts))
                .options(subqueryload(BraRecord.risk_forcasts))
                .options(subqueryload(BraRecord.massif))
            )
            res = s.first()
            return marshal(res, bra_model)


@bra_api.route("/zone")
@bra_api.route("/zone/<uuid:zone_id>")
class ZoneResource(Resource):
    @bra_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")
    @bra_api.response(HTTPStatus.NOT_FOUND, "zone for this id cannot be found.")
    @bra_api.response(HTTPStatus.OK, "OK", zone_model)
    @bra_api.marshal_with(zone_model)
    def get(self, zone_id: Optional[UUID] = None) -> Union[List[Dict], Dict]:
        with session_scope() as sess:
            query = sess.query(Zone).options(subqueryload(Zone.departments))
            if zone_id:
                query.filter(Zone.z_id == zone_id)
            res = query.all()
            if len(res) == 1:
                return res[0]
            return res


@bra_api.route("/departments")
@bra_api.route("/departments/<uuid:department_id>")
class DepartmentResource(Resource):
    @bra_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")
    @bra_api.response(HTTPStatus.NOT_FOUND, "department for this id cannot be found.")
    @bra_api.response(HTTPStatus.OK, "OK", department_model)
    @bra_api.marshal_with(department_model)
    def get(self, department_id: Optional[UUID] = None) -> Dict:
        with session_scope() as sess:
            query = sess.query(Department).options(subqueryload(Department.massifs))
            if department_id:
                query.filter(Department.d_id == department_id)
            return query.all()


@bra_api.route("/massifs")
@bra_api.route("/massifs/<uuid:massif_id>")
class MassifResource(Resource):
    @bra_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")
    @bra_api.response(HTTPStatus.NOT_FOUND, "massif for this id cannot be found.")
    @bra_api.response(HTTPStatus.OK, "OK", FeatureCollectionSchema)
    def get(self, massif_id: UUID = None) -> Dict:
        with connection_scope() as con:
            # alias of table for better reading
            br = BraRecordTable.alias("br")
            m = MassifTable.alias("m")
            d = DepartmentTable.alias("d")

            # Here we want, for each massifs, the last BRA associated.
            # This require some advanced quering (lateral join).
            # the downside is that if you db have no BRA loaded,
            # then this endpoint will return an empty geojson.

            # column we want in the lateral
            lateral_column = [
                m.c.m_id,
                m.c.m_name,
                m.c.the_geom,
                br.c.br_id,
                br.c.br_production_date,
                br.c.br_expiration_date,
                br.c.br_is_amended,
                br.c.br_max_risk,
                br.c.br_risk_comment,
                br.c.br_dangerous_slopes,
                br.c.br_opinion,
                br.c.br_snow_quality,
                br.c.br_snow_stability,
                br.c.br_last_snowfall_date,
                br.c.br_snowlimit_south,
                br.c.br_snowlimit_north,
            ]
            # select the records by production date (desc mean latest).
            lateral = (
                select(lateral_column)
                .where(m.c.m_id == br.c.br_massif)
                .order_by(br.c.br_production_date.desc())
                .limit(1)
                .lateral()
            )
            # selecting everything wrapped up. Also joining on department
            query = (
                select([lateral, d.c.d_id, d.c.d_name, d.c.d_number,])
                .select_from(
                    m.join(lateral, true()).join(d, d.c.d_id == m.c.m_department)
                )
                .order_by(m.c.m_id, lateral.c.br_production_date.desc())
            )
            # if any
            if massif_id:
                query = query.where(m.c.m_id == massif_id)
            lateral_results = con.execute(query).fetchall()
            # transform into json
            results_in_json = marshal(lateral_results, massifs_model)
            features = list()
            for i, result in enumerate(results_in_json):
                risks = con.execute(
                        RiskTable.select(RiskTable.c.r_record_id == result["latest_record"]["id"])
                    ).fetchall()
                result["latest_record"]["risks"] = [
                                    {
                                        "id": r.r_id,
                                        "risk": r.r_risk,
                                        "altitude": r.r_altitude_limit,
                                    }
                                    for r in risks
                                ]
                features.append(Feature(
                    geometry=GeometryField().format(lateral_results[i].the_geom),
                    properties=result
                ))
            if len(features) == 1:
                return jsonify(features[0])
            return jsonify(FeatureCollection(features))
