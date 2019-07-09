import os

from datetime import datetime
from typing import Generator
from uuid import uuid4

import lxml.etree as ET

from lxml import etree
import pytest

from sqlalchemy import text

from nivo_api.cli.bra_record_helper.process import (
    process_xml,
    _get_risk_forcast,
    _get_risk_entity,
    _get_massif_entity,
)
from nivo_api.cli.bra_record_helper.persist import persist_massif
from nivo_api.core.db.connection import connection_scope
from test.pytest_fixtures import setup_db

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestGetMassifEntity:
    @setup_db()
    def test_no_massif(self):
        with connection_scope() as con:
            with pytest.raises(ValueError) as e:
                _get_massif_entity("CHABLAIS", con)
            assert e.value.args[0] == "Cannot found massif CHABLAIS in the db"
            assert e.type is ValueError

    @setup_db()
    def test_massif(self):
        with connection_scope() as con:
            persist_massif(
                con,
                "CHABLAIS",
                {"name": "Haute-savoie", "number": "74"},
                "Alpes du Nord",
            )


class TestGetRiskEntity:
    def test_get_risk_entity_none(self):
        with connection_scope() as con:
            res = _get_risk_entity("", con)
            assert res == None

    @setup_db()
    def test_get_risk_entity_not_exist(self):
        with connection_scope() as con:
            with pytest.raises(ValueError) as e:
                _get_risk_entity("1", con)
            assert (
                e.value.args[0] == "Risk could not be found for level 1 found in bra."
            )

    @setup_db()
    def test_get_risk_entity_exist(self):
        with connection_scope() as con:
            risk_id = uuid4()
            con.execute(
                text("INSERT INTO bra_risk VALUES (:id, :number, :desc)"),
                id=risk_id,
                number=1,
                desc="this is a test",
            )
            res = _get_risk_entity("1", con)
            assert res == risk_id

    def test_get_risk_forcast_work(self):
        with connection_scope() as con:
            xml = etree.parse(
                os.path.join(CURRENT_DIR, "BRA.CHABLAIS.20190101142328.xml")
            )
            bra_id = uuid4()
            x = _get_risk_forcast(xml, bra_id)
            assert isinstance(x, Generator)
            res = next(x)
            assert {
                "rf_bra_record": bra_id,
                "rf_date": datetime(
                    year=2019, month=1, day=3, hour=0, minute=0, second=0
                ),
                "rf_evolution": "STABLE",
            } == res
            res = next(x)
            assert {
                "rf_bra_record": bra_id,
                "rf_date": datetime(
                    year=2019, month=1, day=4, hour=0, minute=0, second=0
                ),
                "rf_evolution": "STABLE",
            } == res
            with pytest.raises(StopIteration):
                next(x)


class TestProcessXML:
    @setup_db()
    def test_process_xml_yield(self):
        # TODO this test need more test data
        with open(
            os.path.join(CURRENT_DIR, "BRA.CHABLAIS.20190101142328.xml"), "rb"
        ) as xmlfile:
            with connection_scope() as c:
                xml = ET.parse(xmlfile)
                p = process_xml(c, xml)
                assert next(p)
                assert next(p)
                assert next(p)
                assert next(p)
                assert next(p)
                with pytest.raises(StopIteration) as e:
                    next(p)
                assert e.type is StopIteration
