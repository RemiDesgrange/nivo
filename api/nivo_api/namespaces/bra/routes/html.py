"""
serve BRA HTML and static stuff related
"""
import os
from datetime import datetime
from uuid import UUID

import lxml.etree as ET
from bs4 import BeautifulSoup
from flask import Response, send_file
from flask_restx import Resource
from flask_restx._http import HTTPStatus
from lxml.etree import _Element, LxmlError
from pkg_resources import resource_stream, resource_filename
from sqlalchemy import select, cast, Date
from sqlalchemy.orm.exc import NoResultFound

from nivo_api.core.db.connection import connection_scope, session_scope
from nivo_api.core.db.models.orm.bra import Massif, BraRecord
from nivo_api.core.db.models.sql.bra import BraRecordTable
from nivo_api.namespaces.bra.namespace import bra_api


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
            res = con.execute(query).first()
        if not res:
            bra_api.abort(HTTPStatus.NOT_FOUND)
        return res.br_raw_xml

    def _transform_bra(self, bra: _Element) -> str:
        try:
            with resource_stream("nivo_api", "static/bra.xslt") as fp:
                xslt = ET.parse(fp)
            transform = ET.XSLT(xslt)
            return str(transform(bra))
        except LxmlError:
            return bra_api.abort(
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
        scripts = soup.find_all("script")
        for script in scripts:
            script["src"] = f"/bra/static/{script['src']}"
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
        with session_scope() as sess:
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d")
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
            except ValueError:
                # strptime fail
                bra_api.abort(HTTPStatus.NOT_FOUND, "BRA for this date or name cannot be found.")

    def _transform_bra(self, bra: _Element) -> str:
        try:
            with resource_stream("nivo_api", "static/bra.xslt") as fp:
                xslt = ET.parse(fp)
            transform = ET.XSLT(xslt)
            return str(transform(bra))
        except LxmlError:
            return bra_api.abort(
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


@bra_api.route("/static/<path:assets>")
class ImagesResource(Resource):
    @bra_api.doc(False)
    def get(self, assets: str = "", massif: str = None):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        if massif:
            assets.replace(massif, "")
        filename = resource_filename("nivo_api", "static/"+assets)
        return send_file(filename)
