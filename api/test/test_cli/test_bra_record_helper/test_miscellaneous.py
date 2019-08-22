import json
import os
from datetime import datetime
from uuid import uuid4

from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from lxml import etree
import pytest
import responses
from freezegun import freeze_time
from unittest.mock import patch, mock_open

from sqlalchemy.engine import Connection

from nivo_api.cli.bra_record_helper.miscellaneous import (
    get_last_bra_date,
    get_bra_xml,
    get_massif_geom,
    check_bra_record_exist,
)
from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.bra import Zone, Department, Massif, BraRecord

from nivo_api.settings import Config
from test.pytest_fixtures import setup_db

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


# make it so it doesn't exist
# bra are served from december to april/may
@freeze_time("2019-09-10")
def test_get_last_bra_date_fail():
    with pytest.raises(AssertionError) as e:
        get_last_bra_date()
    assert str(e.value) == "Bra list does not exist for 2019-09-10"


class TestGetBraDate:
    @responses.activate
    @freeze_time("2019-01-01")
    def test_get_last_date_work(self):
        with open(os.path.join(CURRENT_DIR, "test_data/bra.20190101.json")) as bra_json:
            responses.add(
                responses.GET,
                Config.BRA_BASE_URL + f"/bra.20190101.json",
                json=json.load(bra_json),
            )
        res = get_last_bra_date()
        assert "CHABLAIS" in res
        # in the file, we check that we get the last element of a list (call of to the method pop())
        assert res["ASPE-OSSAU"] == datetime.strptime("20190101135359", "%Y%m%d%H%M%S")
        assert len(res.keys()) == 36

    @responses.activate
    @freeze_time("2019-01-01")
    def test_get_last_date_malformed_json(self):
        with open(
            os.path.join(CURRENT_DIR, "test_data/bra.malformed.json")
        ) as bra_json:
            responses.add(
                responses.GET,
                Config.BRA_BASE_URL + f"/bra.20190101.json",
                json=json.load(bra_json),
            )
        with pytest.raises(ValueError) as e:
            get_last_bra_date()
        assert str(e.value) == "JSON provided is malformed. Cannot parse"


class TestGetBraXml:
    @responses.activate
    def test_get_bra_xml_fail(self):
        responses.add(
            responses.GET,
            Config.BRA_BASE_URL + f"/BRA.CHABLAIS.20190101142328.xml",
            body="bla bla",
            status=302,
        )
        with pytest.raises(AssertionError) as e:
            get_bra_xml("CHABLAIS", datetime.strptime("20190101142328", "%Y%m%d%H%M%S"))
        assert (
            str(e.value)
            == "The bra for the massif CHABLAIS at day 2019-01-01 14:23:28 doesn't exist, status: 302"
        )

    @responses.activate
    def test_get_bra_xml_work(self):
        with open(
            os.path.join(CURRENT_DIR, "test_data/BRA.CHABLAIS.20190101142328.xml")
        ) as bra_xml:
            responses.add(
                responses.GET,
                Config.BRA_BASE_URL + f"/BRA.CHABLAIS.20190101142328.xml",
                body=bra_xml.read(),
                content_type="text/xml",
            )

            res = get_bra_xml(
                "CHABLAIS", datetime.strptime("20190101142328", "%Y%m%d%H%M%S")
            )
        assert isinstance(res, etree._ElementTree)


class TestGetMassifGeom:
    def test_unknown_massif(self):
        with pytest.raises(ValueError) as e:
            get_massif_geom("xyz")
        assert e.type is ValueError
        assert str(e.value) == "Massif xyz geometry cannot be found."

    def test_known_massif(self):
        massif = get_massif_geom("CHABLAIS")
        assert isinstance(massif, WKBElement)

    def test_case_sensivity(self):
        massif = get_massif_geom("ChAblAis")
        assert isinstance(massif, WKBElement)

    def test_geometry_returned(self):
        data = """
        {
            "features": [
                {
                    "geometry": {
                        "coordinates": [
                            [
                                [1,1],[1,2],[2,2],[2,1]
                            ]
                        ],
                        "type": "Polygon"
                    },
                    "properties": {
                        "id": "OPP150",
                        "label": "Renoso",
                        "slug": "renoso"
                    },
                    "type": "Feature"
                }
            ],
            "type": "FeatureCollection"
        }
        """
        with patch("builtins.open", mock_open(read_data=data)):
            ret = get_massif_geom("ReNoSo")
            assert to_shape(ret).wkt == "POLYGON ((1 1, 1 2, 2 2, 2 1, 1 1))"

    def test_massif_have_same_name(self):
        data = """
        {
            "features": [
                {
                    "geometry": {
                        "coordinates": [
                            [
                                [1,1],[1,2],[2,2],[2,1]
                            ]
                        ],
                        "type": "Polygon"
                    },
                    "properties": {
                        "id": "OPP150",
                        "label": "Renoso",
                        "slug": "renoso"
                    },
                    "type": "Feature"
                },
                {
                    "geometry": {
                        "coordinates": [
                            [
                                [2,2],[2,3],[3,3],[3,2]
                            ]
                        ],
                        "type": "Polygon"
                    },
                    "properties": {
                        "id": "OPP150",
                        "label": "Renoso",
                        "slug": "renoso"
                    },
                    "type": "Feature"
                }
            ],
            "type": "FeatureCollection"
        }
        """
        with patch("builtins.open", mock_open(read_data=data)):
            ret = get_massif_geom("ReNoSo")
            assert to_shape(ret).wkt == "POLYGON ((1 1, 1 2, 2 2, 2 1, 1 1))"


class TestFetchDepartmentGeomFromOpendata:
    pass


class TestCheckBraRecordExist:
    def load_data(self, con: Connection, bra_date: datetime) -> None:
        zone_id = con.execute(
            Zone.insert().values(bz_name="test").returning(Zone.c.bz_id)
        ).first()[0]
        dept_id = con.execute(
            Department.insert()
            .values(bd_name="test", bd_zone=zone_id)
            .returning(Department.c.bd_id)
        ).first()[0]
        massif_id = con.execute(
            Massif.insert()
            .values(
                bm_name="test",
                bm_department=dept_id,
                the_geom="SRID=4326;POLYGON((1 1, 1 2, 2 2, 2 1, 1 1))",
            )
            .returning(Massif.c.bm_id)
        ).first()[0]
        con.execute(
            BraRecord.insert().values(
                br_massif=massif_id,
                br_production_date=bra_date,
                br_expiration_date=bra_date,
                br_max_risk=2,
                br_raw_xml="<test></test>",
            )
        )

    @setup_db()
    def test_empty_db(self):
        """
        an empty db should return false
        """
        with connection_scope() as con:
            r = check_bra_record_exist(con, "CHABLAIS", datetime.now())
        assert r is False

    @setup_db()
    @freeze_time("2019-01-01")
    def test_already_exist_record(self):
        with connection_scope() as con:
            self.load_data(con, datetime.now())
            r = check_bra_record_exist(con, "test", datetime.now())
        assert r is True
