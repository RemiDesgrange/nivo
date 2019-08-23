import os
from typing import Optional, Dict
from uuid import UUID
from flask import Response, send_file
from flask_restplus import Namespace, Resource, fields
from flask_restplus._http import HTTPStatus
from lxml.etree import _Element, LxmlError
import lxml.etree as ET
from sqlalchemy import select
from sqlalchemy.orm import relationship, subqueryload

from nivo_api.core.api_schema.geojson import (
    Feature as FeatureSchema,
    FeatureCollection as FeatureCollectionSchema,
)
from nivo_api.core.db.connection import connection_scope, session_scope, DBSession
from nivo_api.core.db.models.orm.bra import Massif, Department
from nivo_api.core.db.models.sql.bra import (
    BraRecordTable,
    ZoneTable,
    DepartmentTable,
)
from nivo_api.namespaces.utils import UUIDField

bra_api = Namespace("bra-api", path="/bra")
bra_api.add_model("Feature", FeatureSchema)
bra_api.add_model("FeatureCollection", FeatureCollectionSchema)

department_massif_model = bra_api.model('MassifModel', {
    "id": UUIDField(attribute="m_id"),
    "name": fields.String(attribute="m_name")
})

department_model = bra_api.model("DepartmentModel", {
    "id": UUIDField(attribute="d_id"),
    "name": fields.String(attribute="d_name"),
    "number": fields.Integer(attribute="d_number"),
    "massifs": fields.List(fields.Nested(department_massif_model))
})


@bra_api.route("/html/<uuid:id>")
class GenerateBRAResource(Resource):
    @bra_api.produces("text/html")
    @bra_api.response(HTTPStatus.BAD_REQUEST, "UUID is invalid.")
    @bra_api.response(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        "Something went wrong in the BRA generation process.",
    )
    @bra_api.response(HTTPStatus.NOT_FOUND, "BRA for this date or id cannot be found.")
    @bra_api.param("id", "The UUID of the bra you want to request")
    def get(self, id: UUID) -> Response:
        bra = self._get_bra_by_uuid_or_404(id)
        html = self._transform_bra(bra)
        return Response(html)

    def _get_bra_by_uuid_or_404(self, bra_id: UUID) -> _Element:
        with connection_scope() as con:
            query = select([BraRecordTable.c.br_raw_xml]).where(
                BraRecordTable.c.br_id == bra_id
            )
            res = con.execute(query).first().br_raw_xml
        if not res:
            bra_api.abort(HTTPStatus.NOT_FOUND)
        return res

    def _transform_bra(self, bra: _Element) -> str:
        try:
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            xslt = ET.parse(os.path.join(cur_dir, "../../static/bra.xslt"))
            transform = ET.XSLT(xslt)
            return str(transform(bra))
        except LxmlError:
            bra_api.abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Something went wrong in BRA generation 😭",
            )


@bra_api.route("/html/<string:massif>/<string:date>")
class GenerateBRAByDateResource(Resource):
    @bra_api.produces("text/html")
    @bra_api.response(
        HTTPStatus.BAD_REQUEST, "If date cannot be parsed or massif is invalid."
    )
    @bra_api.response(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        "Something went wrong in the BRA generation process.",
    )
    @bra_api.response(HTTPStatus.NOT_FOUND, "BRA for this date or id cannot be found.")
    @bra_api.param("id", "The date of the bra you want to request")
    @bra_api.param("massif", "the massifs you want to request")
    def get(self, id: UUID) -> Response:
        bra = self._get_bra_by_uuid_or_404(id)
        html = self._transform_bra(bra)
        return Response(html)


@bra_api.route("/zone")
@bra_api.route("/zone/<uuid:zone_id>")
class ZoneResource(Resource):
    @bra_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")
    @bra_api.response(HTTPStatus.NOT_FOUND, "zone for this id cannot be found.")
    @bra_api.response(
        HTTPStatus.OK, "OK", (FeatureSchema, FeatureCollectionSchema)
    )  # TODO only taking care of Features
    def get(self, zone_id: Optional[UUID] = None) -> Dict:
        with connection_scope() as con:
            j = ZoneTable.join(
                DepartmentTable, DepartmentTable.c.bd_zone == ZoneTable.c.bz_id
            )
            s = select().select_from(j)
            if zone_id:
                s.where(ZoneTable.c.bz_id == zone_id)
            raw_result = con.execute(s).fetchall()
            return raw_result


@bra_api.route("/departments")
@bra_api.route("/departments/<uuid:department_id>")
class DepartmentResource(Resource):
    @bra_api.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")
    @bra_api.response(HTTPStatus.NOT_FOUND, "department for this id cannot be found.")
    @bra_api.response(
        HTTPStatus.OK, "OK", department_model)
    @bra_api.marshal_with(department_model)
    def get(self, departement_id: Optional[UUID] = None) -> Dict:
        with session_scope() as sess:
            query = sess.query(Department).options(subqueryload(Department.massifs))
            if departement_id:
                query.filter(Department.d_id == departement_id)
            return query.all()


@bra_api.route("/html/BRA.css")
@bra_api.route("/html/<path:assets>")
class AssetsResource(Resource):
    @bra_api.doc(False)
    def get(self, assets: str = None):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        if not assets:
            assets = "BRA.css"
        filename = os.path.join(cur_dir, "../../static", assets)
        return send_file(filename)
