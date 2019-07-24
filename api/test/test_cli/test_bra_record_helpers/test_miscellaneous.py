import json
import os
from datetime import datetime

from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from lxml import etree
import pytest
import responses
from freezegun import freeze_time
from unittest.mock import patch, mock_open

from nivo_api.cli.bra_record_helper.miscellaneous import (
    get_last_bra_date,
    get_bra_xml,
    fetch_department_geom_from_opendata,
    get_massif_geom,
)

from nivo_api.settings import Config

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestFetchDepartementGeojsonFromOpenData:
    @responses.activate
    def test_exist(self):
        with open(
                os.path.join(CURRENT_DIR, "departement-74-haute-savoie.geojson")
        ) as dept_json:
            responses.add(
                responses.GET,
                "https://france-geojson.gregoiredavid.fr/repo/departements/74-haute-savoie/departement-74-haute-savoie.geojson",
                json=json.load(dept_json),
            )

        # dept num is a string, see massifs.json file, bc we can have for exemple "01" as dept.
        ret = fetch_department_geom_from_opendata("Haute-Savoie", "74")
        assert isinstance(ret, WKBElement)

    @responses.activate
    def test_non_existant_dept(self):
        responses.add(
            responses.GET,
            "https://france-geojson.gregoiredavid.fr/repo/departements/10-haute-savoie/departement-10-haute-savoie.geojson",
            status=404,
        )
        with pytest.raises(AssertionError) as e:
            fetch_department_geom_from_opendata("Haute-Savoie", "10")
        assert (
                str(e.value)
                == "Something went wrong with department geometry fetching from the internet, status: 404"
        )


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
        with open(os.path.join(CURRENT_DIR, "bra.20190101.json")) as bra_json:
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
        with open(os.path.join(CURRENT_DIR, "bra.malformed.json")) as bra_json:
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
                os.path.join(CURRENT_DIR, "BRA.CHABLAIS.20190101142328.xml")
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
            assert to_shape(ret).wkt== "POLYGON ((1 1, 1 2, 2 2, 2 1, 1 1))"



class TestFetchDepartmentGeomFromOpendata:
    pass
