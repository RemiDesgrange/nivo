from typing import Optional, Dict, List, Union
from uuid import UUID

from flask import jsonify
from flask_restx import Resource, marshal
from flask_restx._http import HTTPStatus
from geojson import FeatureCollection, Feature
from sqlalchemy import select, Date, func, true, and_
from sqlalchemy.orm import subqueryload
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql.functions import concat

from nivo_api.core.api_schema.geojson import (
    FeatureCollection as FeatureCollectionSchema,
)
from nivo_api.core.db.connection import connection_scope, session_scope
from nivo_api.core.db.models.orm.bra import (
    Massif,
    Department,
    RiskForecast,
    Zone,
    BraRecord,
    Risk,
    SnowRecord,
    FreshSnowRecord,
    WeatherForecast,
)
from nivo_api.core.db.models.sql.bra import (
    DepartmentTable,
    BraRecordTable,
    MassifTable,
    RiskTable,
)
from nivo_api.namespaces.bra.models import (
    bra_model,
    zone_model,
    department_model,
    massifs_model,
)
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
            results = (
                sess.query(
                    BraRecord,
                    func.lag(BraRecord.br_id)
                    .over(
                        order_by=BraRecord.br_production_date,
                        partition_by=BraRecord.br_massif,
                    )
                    .label("previous_bra_id"),
                    func.lead(BraRecord.br_id)
                    .over(
                        order_by=BraRecord.br_production_date,
                        partition_by=BraRecord.br_massif,
                    )
                    .label("next_bra_id"),
                )
                .filter(
                    BraRecord.br_production_date
                    > (func.now() - func.cast(concat(args["limit"], "DAYS"), INTERVAL))
                )
                .filter(BraRecord.br_massif == massif_id)
                .order_by(BraRecord.br_production_date.desc())
                .options(subqueryload(BraRecord.risks))
                .options(subqueryload(BraRecord.snow_records))
                .options(subqueryload(BraRecord.fresh_snow_records))
                .options(subqueryload(BraRecord.weather_forecasts))
                .options(subqueryload(BraRecord.risk_forecasts))
                .options(subqueryload(BraRecord.massif))
                .all()
            )
            final = []
            for res in results:
                encoded_bra_record = marshal(res.BraRecord, bra_model)
                encoded_bra_record["previous_bra_id"] = (
                    str(res.previous_bra_id) if res.previous_bra_id else None
                )
                encoded_bra_record["next_bra_id"] = (
                    str(res.next_bra_id) if res.next_bra_id else None
                )
                final.append(encoded_bra_record)
            return final


@bra_api.route("/last")
class LastBraListResource(Resource):
    @bra_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")
    @bra_api.response(HTTPStatus.NOT_FOUND, "last bra cannot be found.")
    @bra_api.response(HTTPStatus.OK, "OK", bra_model)
    def get(self) -> List[Dict]:
        """
        Return the last record for all massifs.
        """
        with session_scope() as sess:
            results = (
                sess.query(
                    BraRecord,
                    func.lag(BraRecord.br_id)
                    .over(
                        order_by=BraRecord.br_production_date,
                        partition_by=BraRecord.br_massif,
                    )
                    .label("previous_bra_id"),
                    func.lead(BraRecord.br_id)
                    .over(
                        order_by=BraRecord.br_production_date,
                        partition_by=BraRecord.br_massif,
                    )
                    .label("next_bra_id"),
                )
                .filter(
                    BraRecord.br_production_date.cast(Date)
                    == select([func.max(BraRecord.br_production_date.cast(Date))])
                )
                .options(subqueryload(BraRecord.risks))
                .options(subqueryload(BraRecord.snow_records))
                .options(subqueryload(BraRecord.fresh_snow_records))
                .options(subqueryload(BraRecord.weather_forecasts))
                .options(subqueryload(BraRecord.risk_forecasts))
                .options(subqueryload(BraRecord.massif))
            )
            final = []
            for res in results.all():
                encoded_bra_record = marshal(res.BraRecord, bra_model)
                encoded_bra_record["previous_bra_id"] = (
                    str(res.previous_bra_id) if res.previous_bra_id else None
                )
                encoded_bra_record["next_bra_id"] = (
                    str(res.next_bra_id) if res.next_bra_id else None
                )
                final.append(encoded_bra_record)
            return final


@bra_api.route("/record/<uuid:record_id>")
class LastBraListResource(Resource):
    @bra_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")
    @bra_api.response(HTTPStatus.NOT_FOUND, "record for this bra cannot be found.")
    @bra_api.response(HTTPStatus.OK, "OK", bra_model)
    def get(self, record_id: UUID) -> Dict:
        """
        Return a specific BRA with it's ID.
        """
        with session_scope() as sess:
            global_rec = sess.query(
                BraRecord,
                func.lag(BraRecord.br_id)
                .over(
                    order_by=BraRecord.br_production_date,
                    partition_by=BraRecord.br_massif,
                )
                .label("previous_bra_id"),
                func.lead(BraRecord.br_id)
                .over(
                    order_by=BraRecord.br_production_date,
                    partition_by=BraRecord.br_massif,
                )
                .label("next_bra_id"),
            ).subquery()
            result_filtered = (
                sess.query(global_rec).filter(global_rec.c.br_id == record_id).first()
            )
            record_as_dict = result_filtered._asdict()
            # TODO it does not return relationship. Subqueryload doesn't work with subquery.
            record_as_dict["massif"] = (
                sess.query(Massif)
                .filter(Massif.m_id == result_filtered.br_massif)
                .first()
            )
            record_as_dict["risks"] = sess.query(Risk).filter(
                Risk.r_record_id == result_filtered.br_id
            )
            record_as_dict["snow_records"] = sess.query(SnowRecord).filter(
                SnowRecord.s_bra_record == result_filtered.br_id
            )
            record_as_dict["fresh_snow_records"] = sess.query(FreshSnowRecord).filter(
                FreshSnowRecord.fsr_bra_record == result_filtered.br_id
            )
            record_as_dict["weather_forecasts"] = sess.query(WeatherForecast).filter(
                WeatherForecast.wf_bra_record == result_filtered.br_id
            )
            record_as_dict["risk_forecasts"] = sess.query(RiskForecast).filter(
                RiskForecast.rf_bra_record == result_filtered.br_id
            )
            return marshal(record_as_dict, bra_model)


@bra_api.route("/massifs/<uuid:massif_id>/last")
class LastBraRecordResource(Resource):
    @bra_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")
    @bra_api.response(HTTPStatus.NOT_FOUND, "bra for this massif cannot be found.")
    @bra_api.response(HTTPStatus.OK, "OK", bra_model)
    def get(self, massif_id: UUID) -> Dict:
        """
        Return a record for a massifs. With all the associated metadata.
        """
        with session_scope() as sess:
            request = (
                sess.query(BraRecord, func.lag(BraRecord.br_id)
                .over(
                    order_by=BraRecord.br_production_date,
                    partition_by=BraRecord.br_massif,
                )
                .label("previous_bra_id"),
                func.lead(BraRecord.br_id)
                .over(
                    order_by=BraRecord.br_production_date,
                    partition_by=BraRecord.br_massif,
                )
                .label("next_bra_id"))
                .filter(BraRecord.br_massif == massif_id)
                .order_by(BraRecord.br_production_date.desc())
                .limit(1)
            )
            result = request.first()
            json = marshal(result.BraRecord, bra_model)
            json["previous_bra_id"] = result.previous_bra_id
            json["next_bra_id"] = result.next_bra_id
            return json


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
            # Also select if it has a previous and next
            next_bra = (
                select([br.c.br_id.label("next_bra_id")])
                .where(
                    and_(
                        br.c.br_massif == m.c.m_id,
                        br.c.br_production_date > lateral.c.br_production_date,
                    )
                )
                .order_by(br.c.br_production_date.desc())
                .limit(1)
                .lateral()
            )
            previous_bra = (
                select([br.c.br_id.label("previous_bra_id")])
                .where(
                    and_(
                        br.c.br_massif == m.c.m_id,
                        br.c.br_production_date < lateral.c.br_production_date,
                    )
                )
                .order_by(br.c.br_production_date.desc())
                .limit(1)
                .lateral()
            )
            # selecting everything wrapped up. Also joining on department
            query = (
                select(
                    [
                        lateral,
                        d.c.d_id,
                        d.c.d_name,
                        d.c.d_number,
                        next_bra,
                        previous_bra,
                    ]
                )
                .select_from(
                    m.join(lateral, true())
                    .join(d, d.c.d_id == m.c.m_department)
                    .outerjoin(next_bra, true())
                    .outerjoin(previous_bra, true())
                )
                .order_by(m.c.m_id, lateral.c.br_production_date.desc())
            )
            # if any
            if massif_id:
                query = query.where(m.c.m_id == massif_id)
            lateral_results = con.execute(query).fetchall()
            # transform into json
            results_in_json = marshal(lateral_results, massifs_model)
            # print(f"{results_in_json[0].previous_bra_id=}")
            # print(f"{results_in_json[0].next_bra_id=}")
            features = list()
            for i, result in enumerate(results_in_json):
                risks = con.execute(
                    RiskTable.select(
                        RiskTable.c.r_record_id == result["latest_record"]["id"]
                    )
                ).fetchall()
                result["latest_record"]["risks"] = [
                    {
                        "id": r.r_id,
                        "risk": r.r_risk,
                        "altitude": r.r_altitude_limit,
                    }
                    for r in risks
                ]
                features.append(
                    Feature(
                        geometry=GeometryField().format(lateral_results[i].the_geom),
                        properties=result,
                    )
                )
            if len(features) == 1:
                return jsonify(features[0])
            return jsonify(FeatureCollection(features))
