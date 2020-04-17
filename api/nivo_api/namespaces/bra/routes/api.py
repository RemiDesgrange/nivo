import json
from typing import Optional, Dict, List, Union
from uuid import UUID

from flask import jsonify
from flask_restx import Resource, marshal
from flask_restx._http import HTTPStatus
from geojson import FeatureCollection, Feature
from sqlalchemy import select, Date, func, desc, text
from sqlalchemy.orm import subqueryload

from nivo_api.core.api_schema.geojson import (
    FeatureCollection as FeatureCollectionSchema,
)
from nivo_api.core.db.connection import connection_scope, session_scope
from nivo_api.core.db.models.orm.bra import Massif, Department, Zone, BraRecord
from nivo_api.namespaces.bra.models import bra_model, zone_model, department_model
from nivo_api.namespaces.bra.namespace import bra_api


massif_record_parser = bra_api.parser()
massif_record_parser.add_argument("limit", type=int, required=False, default=50)


@bra_api.route("/massifs/<uuid:massif_id>/records")
class MassifsRecordRessource(Resource):
    @bra_api.expect(massif_record_parser)
    def get(self, massif_id: UUID) -> List[Dict]:
        """
        Return a list of records for a massif. Limit to last 50 records (last 50 bra)
        """
        args = massif_record_parser.parse_args()
        with session_scope() as sess:
            res = (
                sess.query(BraRecord)
                .filter(BraRecord.br_massif == massif_id)
                .order_by(desc(BraRecord.br_production_date))
                .limit(args["limit"])
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
                .order_by(desc(BraRecord.br_production_date))
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
    def get(self, departement_id: Optional[UUID] = None) -> Dict:
        with session_scope() as sess:
            query = sess.query(Department).options(subqueryload(Department.massifs))
            if departement_id:
                query.filter(Department.d_id == departement_id)
            return query.all()


@bra_api.route("/massifs")
@bra_api.route("/massifs/<uuid:massif_id>")
class MassifResource(Resource):
    @bra_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")
    @bra_api.response(HTTPStatus.NOT_FOUND, "department for this id cannot be found.")
    @bra_api.response(HTTPStatus.OK, "OK", FeatureCollectionSchema)
    def get(self, massif_id: UUID = None) -> Dict:
        with connection_scope() as con:
            whereclause = ""
            if massif_id:
                whereclause = f"m_id = {massif_id}"

            # no idea how to do this in sqlalchemy
            query = text(
                f"""
            SELECT result.* FROM bra.massif m
                JOIN LATERAL (
                    SELECT ST_AsGeoJSON(m.the_geom) as the_geom, 
m.m_id, 
m.m_name, 
d.d_id, 
d.d_name, 
d.d_number,
r.br_max_risk, 
r.br_production_date::date,
r.br_dangerous_slopes
FROM bra.record r
                        join bra.department d on (d.d_id=m_department)
                        where (m.m_id=r.br_massif)
                    ORDER BY r.br_production_date DESC limit 1
                    ) result on true
                {whereclause}
                ORDER BY m.m_id, result.br_production_date DESC
            """
            )

            features = list()
            for res in con.execute(query):
                features.append(
                    Feature(
                        geometry=json.loads(res.the_geom),
                        properties={
                            "id": res.m_id,
                            "name": res.m_name,
                            "latest_risk": res.br_max_risk,
                            "latest_date": res.br_production_date,
                            "latest_dangerous_slopes": res.br_dangerous_slopes[
                                1:-1
                            ].split(","),
                            "department": {
                                "id": res.d_id,
                                "name": res.d_name,
                                "number": res.d_number,
                            },
                        },
                    )
                )
            if len(features) == 1:
                return jsonify(features[0])
            return jsonify(FeatureCollection(features))
