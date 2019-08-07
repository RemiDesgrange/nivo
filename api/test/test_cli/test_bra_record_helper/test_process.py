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
    _get_dangerous_slopes,
    _get_bra_snow_records,
    _get_fresh_snow_record,
    _get_weather_forcast_at_altitude,
    _get_weather_forcast,
)
from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.bra import DangerousSlopes, WindDirection
from test.pytest_fixtures import setup_db

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def bra_xml_parsed() -> ET._Element:
    with open(
        os.path.join(CURRENT_DIR, "BRA.CHABLAIS.20190101142328.xml"), "rb"
    ) as xmlfile:
        return ET.parse(xmlfile)


class TestGetRiskEntity:
    """
    """

    def test_get_risk_entity_none(self):
        """
        it should return None if the first argument of the function evaluate to false
        """
        with connection_scope() as con:
            res = _get_risk_entity("", con)
            assert res == None

    @setup_db()
    def test_get_risk_entity_not_exist(self):
        """
        it should raise ValueError when entity is not found in db.
        """
        with connection_scope() as con:
            with pytest.raises(ValueError) as e:
                _get_risk_entity("1", con)
            assert (
                e.value.args[0] == "Risk could not be found for level 1 found in bra."
            )

    @setup_db()
    def test_get_risk_entity_exist(self):
        """
        risk exist and it return his id (of form uuid).
        """
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
        xml = etree.parse(os.path.join(CURRENT_DIR, "BRA.CHABLAIS.20190101142328.xml"))
        bra_id = uuid4()
        x = _get_risk_forcast(xml, bra_id)
        assert isinstance(x, Generator)
        res = next(x)
        assert {
            "rf_bra_record": bra_id,
            "rf_date": datetime(year=2019, month=1, day=3, hour=0, minute=0, second=0),
            "rf_evolution": "STABLE",
        } == res
        res = next(x)
        assert {
            "rf_bra_record": bra_id,
            "rf_date": datetime(year=2019, month=1, day=4, hour=0, minute=0, second=0),
            "rf_evolution": "STABLE",
        } == res
        with pytest.raises(StopIteration):
            next(x)


class TestGetMassifEntity:
    @setup_db()
    def test_no_massif(self):
        with connection_scope() as con:
            with pytest.raises(ValueError) as e:
                _get_massif_entity("CHABLAIS", con)
            assert e.value.args[0] == "Cannot found massif CHABLAIS in the db"
            assert e.type is ValueError


"""
Testing wrong XML is useless since it will ne detected before. Also testing for "COMMENT" is useless 'cause of
enumeration (we all love enums)
"""


def test_dangerous_slopes_valid(bra_xml_parsed):
    ret = _get_dangerous_slopes(bra_xml_parsed)
    assert isinstance(ret, list)
    assert len(ret) == 5
    test_sample = [
        DangerousSlopes("NE"),
        DangerousSlopes("E"),
        DangerousSlopes("W"),
        DangerousSlopes("NW"),
        DangerousSlopes("N"),
    ]
    for i, ds in enumerate(ret):
        assert isinstance(ds, DangerousSlopes)
        assert ds == test_sample[i]


def test_get_bra_snow_records(bra_xml_parsed):
    bra_id = uuid4()
    res = _get_bra_snow_records(bra_xml_parsed, bra_id)
    test_data = [
        {
            "s_bra_record": bra_id,
            "s_altitude": 1000,
            "s_snow_quantity_cm_north": 0,
            "s_snow_quantity_cm_south": 0,
        },
        {
            "s_bra_record": bra_id,
            "s_altitude": 1500,
            "s_snow_quantity_cm_north": 20,
            "s_snow_quantity_cm_south": 5,
        },
        {
            "s_bra_record": bra_id,
            "s_altitude": 2000,
            "s_snow_quantity_cm_north": 70,
            "s_snow_quantity_cm_south": 50,
        },
    ]
    for i, sr in enumerate(res):
        assert test_data[i] == sr


def test_get_fresh_snow_record(bra_xml_parsed):
    bra_id = uuid4()
    res = _get_fresh_snow_record(bra_xml_parsed, bra_id)
    test_data = [
        {
            "bfsr_bra_record": bra_id,
            "bfsr_date": datetime(2018, 12, 28, 00, 00, 00),
            "bfsr_altitude": 1800,
            "bsfr_massif_snowfall": 0,
            "bfsr_second_massif_snowfall": -1,
        },
        {
            "bfsr_bra_record": bra_id,
            "bfsr_date": datetime(2018, 12, 29, 00, 00, 00),
            "bfsr_altitude": 1800,
            "bsfr_massif_snowfall": 0,
            "bfsr_second_massif_snowfall": -1,
        },
        {
            "bfsr_bra_record": bra_id,
            "bfsr_date": datetime(2018, 12, 30, 00, 00, 00),
            "bfsr_altitude": 1800,
            "bsfr_massif_snowfall": 0,
            "bfsr_second_massif_snowfall": -1,
        },
        {
            "bfsr_bra_record": bra_id,
            "bfsr_date": datetime(2018, 12, 31, 00, 00, 00),
            "bfsr_altitude": 1800,
            "bsfr_massif_snowfall": 0,
            "bfsr_second_massif_snowfall": -1,
        },
        {
            "bfsr_bra_record": bra_id,
            "bfsr_date": datetime(2019, 1, 1, 00, 00, 00),
            "bfsr_altitude": 1800,
            "bsfr_massif_snowfall": 2,
            "bfsr_second_massif_snowfall": -1,
        },
        {
            "bfsr_bra_record": bra_id,
            "bfsr_date": datetime(2019, 1, 2, 00, 00, 00),
            "bfsr_altitude": 1800,
            "bsfr_massif_snowfall": 3,
            "bfsr_second_massif_snowfall": -1,
        },
    ]
    for i, fsr in enumerate(res):
        assert isinstance(fsr, dict)
        assert fsr == test_data[i]


class TestGetWeatherForcastAtAltitude:
    def test_get_weather_forcast_at_altitude_work(self, bra_xml_parsed):
        wf_id = uuid4()
        record = bra_xml_parsed.find("//METEO").getchildren()[1]
        res = _get_weather_forcast_at_altitude(record, wf_id, 2000, 1)
        assert isinstance(res, dict)
        assert res["wfaa_wind_altitude"] == 2000
        assert res["wfaa_wf_id"] == wf_id
        assert res["wfaa_wind_direction"] == WindDirection.NE

    def test_get_weather_forcast_at_altitude_invalid_index(self, bra_xml_parsed):
        bra_id = uuid4()
        record = bra_xml_parsed.find("//METEO").getchildren()[0]
        with pytest.raises(ValueError) as e:
            _get_weather_forcast_at_altitude(record, bra_id, 2000, 10)
        assert str(e.value) == "Cannot found value for index 10"


class TestGetWeatherForcast:
    def test_get_weather_forcast_work(self, bra_xml_parsed):
        bra_id = uuid4()
        res = _get_weather_forcast(bra_xml_parsed, bra_id)
        assert isinstance(res, Generator)
        for wf in res:
            assert isinstance(wf, dict)
            assert wf["wf_bra_record"] == bra_id
            assert isinstance(wf["wf_expected_date"], datetime)
            assert len(wf["wf_at_altitude"]) == 2


class TestProcessXML:
    @setup_db()
    def test_process_xml_yield(self, bra_xml_parsed):
        with connection_scope() as c:
            p = process_xml(c, bra_xml_parsed)
            assert isinstance(p, list)
