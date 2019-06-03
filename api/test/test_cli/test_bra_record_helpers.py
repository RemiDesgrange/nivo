import json
import os
from contextlib import contextmanager
from datetime import datetime
from typing import Generator
from uuid import uuid4

from geoalchemy2 import Geometry, WKBElement
from lxml import etree
import pytest
import responses
from freezegun import freeze_time
from sqlalchemy import text

from nivo_api.cli.bra_record_helper.miscellaneous import get_last_bra_date, get_bra_xml, \
    fetch_department_geom_from_opendata, build_zone_from_department_geom
from nivo_api.cli.bra_record_helper.process import process_xml, _get_risk_forcast, _get_risk_entity, _get_massif_entity
from nivo_api.cli.bra_record_helper.persist import persist_massif
from nivo_api.core.db.connection import metadata, db_engine, connection_scope
from nivo_api.settings import Config

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@contextmanager
def setup_db():
    metadata.drop_all(db_engine)
    metadata.create_all(db_engine)
    yield
    metadata.drop_all(db_engine)


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
        with open(os.path.join(CURRENT_DIR, 'bra.20190101.json')) as bra_json:
            responses.add(responses.GET, Config.BRA_BASE_URL + f'/bra.20190101.json',
                          json=json.load(bra_json))
        res = get_last_bra_date()
        assert 'CHABLAIS' in res
        # in the file, we check that we get the last element of a list (call of to the method pop())
        assert res["ASPE-OSSAU"] == datetime.strptime('20190101135359', '%Y%m%d%H%M%S')
        assert len(res.keys()) == 36

    @responses.activate
    @freeze_time("2019-01-01")
    def test_get_last_date_malformed_json(self):
        with open(os.path.join(CURRENT_DIR, 'bra.malformed.json')) as bra_json:
            responses.add(responses.GET, Config.BRA_BASE_URL + f'/bra.20190101.json',
                          json=json.load(bra_json))
        with pytest.raises(ValueError) as e:
            get_last_bra_date()
        assert str(e.value) == 'JSON provided is malformed. Cannot parse'


class TestGetBraXml:
    @responses.activate
    def test_get_bra_xml_fail(self):
        responses.add(responses.GET, Config.BRA_BASE_URL + f'/BRA.CHABLAIS.20190101142328.xml',
                      body='bla bla',
                      status=302)
        with pytest.raises(AssertionError) as e:
            get_bra_xml('CHABLAIS', datetime.strptime('20190101142328', '%Y%m%d%H%M%S'))
        assert str(e.value) == "The bra for the massif CHABLAIS at day 2019-01-01 14:23:28 doesn't exist"

    @responses.activate
    def test_get_bra_xml_work(self):
        with open(os.path.join(CURRENT_DIR, 'BRA.CHABLAIS.20190101142328.xml')) as bra_xml:
            responses.add(responses.GET, Config.BRA_BASE_URL + f'/BRA.CHABLAIS.20190101142328.xml',
                          body=bra_xml.read(),
                          content_type='text/xml')

            res = get_bra_xml('CHABLAIS', datetime.strptime('20190101142328', '%Y%m%d%H%M%S'))
        assert isinstance(res, etree._Element)


class TestGetRiskEntity:
    def test_get_risk_entity_none(self):
        with connection_scope() as con:
            res = _get_risk_entity('', con)
            assert res == None

    @setup_db()
    def test_get_risk_entity_not_exist(self):
        with connection_scope() as con:
            with pytest.raises(ValueError) as e:
                res = _get_risk_entity('1', con)
            assert e.value == "Risk could not be found for level 1 found in bra."

    @setup_db()
    def test_get_risk_entity_exist(self):
        with connection_scope() as con:
            risk_id = uuid4()
            con.execute(text("INSERT INTO bra_risk VALUES (:id, :number, :desc)"),
                        id=risk_id,
                        number=1,
                        desc='this is a test')
            res = _get_risk_entity('1', con)
            assert res == risk_id

    def test_get_risk_forcast_work(self):
        with connection_scope() as con:
            xml = etree.parse(os.path.join(CURRENT_DIR, 'BRA.CHABLAIS.20190101142328.xml'))
            bra_id = uuid4()
            x = _get_risk_forcast(xml, bra_id)
            assert isinstance(x, Generator)
            res = next(x)
            assert {
                       'rf_bra_record': bra_id,
                       'rf_date': datetime(year=2019, month=1, day=3, hour=0, minute=0, second=0),
                       'rf_evolution': 'STABLE'
                   } == res
            res = next(x)
            assert {
                       'rf_bra_record': bra_id,
                       'rf_date': datetime(year=2019, month=1, day=4, hour=0, minute=0, second=0),
                       'rf_evolution': 'STABLE'
                   } == res
            with pytest.raises(StopIteration):
                next(x)


class TestGetMassifEntity:
    @setup_db()
    def test_no_massif(self):
        with connection_scope() as con:
            with pytest.raises(ValueError) as e:
                _get_massif_entity('CHABLAIS', con)
            assert e.value == 'Cannot found massif CHABLAIS in the db'

    @setup_db()
    def test_massif(self):
        with connection_scope() as con:
            persist_massif(con, 'CHABLAIS', {'nom_dept': 'Haute-savoie', "num_dept": '74'}, 'Alpes du Nord')


class TestFetchDepartementGeojsonFromOpenData:
    @responses.activate
    def test_exist(self):
        with open(os.path.join(CURRENT_DIR, 'departement-74-haute-savoie.geojson')) as dept_json:
            responses.add(responses.GET, 'https://france-geojson.gregoiredavid.fr/repo/departements/74-haute-savoie/departement-74-haute-savoie.geojson',
                          json=json.load(dept_json))

        # dept num is a string, see massifs.json file, bc we can have for exemple "01" as dept.
        ret = fetch_department_geom_from_opendata('Haute-Savoie', '74')
        assert isinstance(ret, WKBElement)


    @responses.activate
    def test_non_existant_dept(self):
        responses.add(responses.GET, 'https://france-geojson.gregoiredavid.fr/repo/departements/10-haute-savoie/departement-10-haute-savoie.geojson', status=404)
        with pytest.raises(AssertionError) as e:
            fetch_department_geom_from_opendata('Haute-Savoie', '10')
        assert str(e.value) == 'Something went wrong with department geometry fetching from the internet'


class TestUnionDeptToHaveAZoneGeometry:
    def test_xxxxx(self):
        build_zone_from_department_geom()