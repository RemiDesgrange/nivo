import os
from datetime import datetime
from typing import Optional, Dict, List, Union
from uuid import UUID

from bs4 import BeautifulSoup
from flask import Response, send_file
from flask_restplus import Namespace, Resource, fields
from flask_restplus._http import HTTPStatus
from lxml.etree import _Element, LxmlError
import lxml.etree as ET
from sqlalchemy import select, cast, Date, and_, func, desc
from sqlalchemy.orm import subqueryload
from sqlalchemy.orm.exc import NoResultFound

from nivo_api.core.api_schema.geojson import (
    Feature as FeatureSchema,
    FeatureCollection as FeatureCollectionSchema,
)
from nivo_api.core.db.connection import connection_scope, session_scope
from nivo_api.core.db.models.orm.bra import Massif, Department, Zone, BraRecord
from nivo_api.core.db.models.sql.bra import BraRecordTable, MassifTable
from nivo_api.namespaces.utils import UUIDField, GeometryField
from geojson import FeatureCollection, Feature

bra_api = Namespace("bra-api", path="/bra")
bra_api.add_model("Feature", FeatureSchema)
bra_api.add_model("FeatureCollection", FeatureCollectionSchema)

zone_model = bra_api.model(
    "ZoneModel",
    {
        "id": UUIDField(attribute="z_id"),
        "name": fields.String(attribute="z_name"),
        "departments": fields.List(
            fields.Nested(
                bra_api.model(
                    "ZoneDepartmentModel",
                    {
                        "id": UUIDField(attribute="d_id"),
                        "name": fields.String(attribute="d_name"),
                        "number": fields.Integer(attribute="d_number"),
                    },
                )
            )
        ),
    },
)

department_model = bra_api.model(
    "DepartmentModel",
    {
        "id": UUIDField(attribute="d_id"),
        "name": fields.String(attribute="d_name"),
        "number": fields.Integer(attribute="d_number"),
        "massifs": fields.List(
            fields.Nested(
                bra_api.model(
                    "DepartmentMassifModel",
                    {
                        "id": UUIDField(attribute="m_id"),
                        "name": fields.String(attribute="m_name"),
                    },
                )
            )
        ),
    },
)

bra_model = bra_api.model('BraModel', {
    "id": UUIDField(attribute="br_id"),
    "production_date": fields.DateTime(attribute="br_production_date"),
    "expiration_date": fields.DateTime(attribute="br_expiration_date"),
    "max_risk": fields.Integer(attribute="br_max_risk"),
    "risk_comment": fields.String(attribute="br_risk_comment"),
    "dangerous_slopes": fields.List(fields.String, attribute='br_dangerous_slopes'),
    "dangerous_slopes_comment": fields.String(attribute="br_dangerous_slopes_comment"),
    "opinion": fields.String(attribute="br_opinion"),
    "snow_quality": fields.String(attribute="br_snow_quality"),
    "last_snowfall_date": fields.DateTime(attribute="br_last_snowfall_date"),
    "snowlimit_south": fields.Integer(attribute="br_snowlimit_south"),
    "snowlimit_north": fields.Integer(attribute="br_snowlimit_north"),
    "massif": fields.Nested(
        bra_api.model("BraMassifModel", {
            "id": UUIDField(attribute="m_id"),
            "name": fields.String(attribute="m_name")
        })
    )
})


@bra_api.route("/html/<uuid:id>")
class GenerateBraHtmlResource(Resource):
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
        cleaned_html = self._change_img_and_css_tag(html)
        return Response(cleaned_html)

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

    def _change_img_and_css_tag(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        img_tags = soup.find_all("img")
        for img in img_tags:
            if img["src"].startswith("Images"):
                img["src"] = f"/bra/static/{img['src']}"
        # css
        links = soup.find_all("link")
        for link in links:
            link["href"] = f"/bra/static/{link['href']}"
        # Also need to modify CSS "background" in the html
        return str(soup)


@bra_api.route("/html/<string:massif>/<string:date>")
class GenerateBraHmlByDateResource(Resource):
    @bra_api.produces("text/html")
    @bra_api.response(
        HTTPStatus.BAD_REQUEST, "If date cannot be parsed or massif is invalid."
    )
    @bra_api.response(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        "Something went wrong in the BRA generation process.",
    )
    @bra_api.response(
        HTTPStatus.NOT_FOUND, "BRA for this date or name cannot be found."
    )
    @bra_api.param("date", "The date of the bra you want to request. format: %Y-%m-%d")
    @bra_api.param("massif", "the massifs you want to request")
    def get(self, massif: str, date: str) -> Response:
        bra = self._get_bra_by_date_or_404(massif, date)
        html = self._transform_bra(bra)
        cleaned_html = self._change_img_and_css_tag(html)
        return Response(cleaned_html)

    def _get_bra_by_date_or_404(self, massif: str, date: str) -> _Element:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        with session_scope() as sess:
            try:
                query = (
                    sess.query(BraRecord.br_raw_xml)
                        .join(Massif)
                        .filter(Massif.m_name == massif.upper())
                        .filter(cast(BraRecord.br_production_date, Date) == parsed_date)
                )
                return query.one().br_raw_xml
            except NoResultFound:
                bra_api.abort(
                    HTTPStatus.NOT_FOUND, "BRA for this date or name cannot be found."
                )

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

    def _change_img_and_css_tag(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        img_tags = soup.find_all("img")
        for img in img_tags:
            if img["src"].startswith("Images"):
                img["src"] = f"/bra/static/{img['src']}"
        # css
        links = soup.find_all("link")
        for link in links:
            link["href"] = f"/bra/static/{link['href']}"
        return str(soup)


@bra_api.route('/last')
class LastBraListResource(Resource):
    @bra_api.marshal_with(bra_model)
    def get(self) -> Dict:
        with connection_scope() as con:
            col = list(BraRecordTable.c)
            col.append(MassifTable.c.m_name)
            col.append(MassifTable.c.m_id)
            join = BraRecordTable.join(MassifTable)
            s = (select(col).select_from(join)
                 .where(BraRecordTable.c.br_production_date.cast(Date) == select(
                [func.max(BraRecordTable.c.br_production_date.cast(Date))]))
                 )
            res = con.execute(s).fetchall()
            return res


@bra_api.route('/<uuid:massif_id>/last')
class LastBraResource(Resource):
    @bra_api.marshal_with(bra_model)
    def get(self, massif_id: UUID) -> Dict:
        with connection_scope() as con:
            s = (select(BraRecordTable.c)
                 .where(BraRecordTable.c.br_massif == massif_id)
                 .order_by(desc(BraRecordTable.c.br_production_date)).limit(1)
                 )
            res = con.execute(s).first()
            return res


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
        with session_scope() as sess:
            query = sess.query(Massif).options(subqueryload(Massif.department))
            if massif_id:
                query = query.filter(Massif.m_id == massif_id)
            features = list()
            for res in query:
                features.append(
                    Feature(
                        geometry=GeometryField().format(res.the_geom),
                        properties={
                            "id": res.m_id,
                            "name": res.m_name,
                            "department": {
                                "id": res.department.d_id,
                                "name": res.department.d_name,
                                "number": res.department.d_number,
                            },
                        },
                    )
                )
            if len(features) == 1:
                return features[0]
            return FeatureCollection(features)


class CssResource(Resource):
    @bra_api.doc(False)
    def get(self, massifs: str = None) -> Response:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(cur_dir, "../../static/BRA.css")
        return send_file(filename)


@bra_api.route("/static/<path:assets>")
class ImagesResource(Resource):
    @bra_api.doc(False)
    def get(self, assets: str = None, massif: str = None):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        if massif:
            assets.replace(massif, "")
        filename = os.path.join(cur_dir, "../../static/", assets)
        return send_file(filename)
