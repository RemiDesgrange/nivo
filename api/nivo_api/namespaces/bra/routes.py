import os
from datetime import date, datetime
from io import BytesIO
from typing import Union
from uuid import UUID

from flask import Response, send_file
from flask_restplus import Namespace, Resource, abort
from flask_restplus._http import HTTPStatus
from lxml.etree import _Element
import lxml.etree as ET
from sqlalchemy import select

from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.bra import BraRecord

bra_api = Namespace("bra-api", path="/bra")


@bra_api.route("/html/<string:id>")
@bra_api.route("/html/<uuid:id>")
class GenerateBRAResource(Resource):
    @bra_api.produces("text/html")
    @bra_api.response(
        HTTPStatus.BAD_REQUEST, "If date cannot be parsed or UUID is invalid."
    )
    @bra_api.response(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        "Something went wrong in the BRA generation process.",
    )
    @bra_api.response(HTTPStatus.NOT_FOUND, "BRA for this date or id cannot be found.")
    @bra_api.param("id", "The UUID or the date of the bra you want to request")
    def get(self, id: Union[UUID, str]) -> Response:
        bra: _Element
        if isinstance(id, UUID):
            bra = self._get_bra_by_uuid_or_404(id)
        elif isinstance(id, str):
            bra_date = self._parse_date_or_fail(id)
            bra = self._get_bra_by_date_or_404(bra_date)
        else:
            return bra_api.abort(
                code=HTTPStatus.BAD_REQUEST, message="Cannot understand your parameters"
            )
        html = self._transform_bra(bra)
        return Response(html)

    def _get_bra_by_uuid_or_404(self, bra_id: UUID) -> _Element:
        with connection_scope() as con:
            query = select([BraRecord.c.br_raw_xml]).where(BraRecord.c.br_id == bra_id)
            res = con.execute(query).first().br_raw_xml
        if not res:
            bra_api.abort(HTTPStatus.NOT_FOUND)
        return res

    def _get_bra_by_date_or_404(self, bra_date: date) -> _Element:
        with connection_scope() as con:
            query = select([BraRecord.c.br_raw_xml]).where(
                BraRecord.c.br_production_date == bra_date
            )
            res = con.execute(query).first().br_raw_xml
        if not res:
            bra_api.abort(HTTPStatus.NOT_FOUND)
        return res

    def _parse_date_or_fail(self, bra_date: str) -> date:
        try:
            return datetime.strptime(bra_date, "%Y-%m-%d").date()
        except ValueError as e:
            abort(
                code=HTTPStatus.BAD_REQUEST,
                message=f"cannot understand date {bra_date}. Format is %Y-%m-%d",
            )

    def _transform_bra(self, bra: _Element) -> str:
        try:
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            xslt = ET.parse(os.path.join(cur_dir, "../../static/bra.xslt"))
            transform = ET.XSLT(xslt)
            return str(transform(bra))
        except:
            bra_api.abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Something went wrong in BRA generation 😭",
            )


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
