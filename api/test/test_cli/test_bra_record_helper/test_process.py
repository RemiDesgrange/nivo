import os

from datetime import datetime
from typing import Generator
from uuid import uuid4

import lxml.etree as ET
import pytest
from test.pytest_fixtures import database

from nivo_api.cli.bra_record_helper.process import (
    process_xml,
    _get_massif_id,
    _get_dangerous_slopes,
    _get_bra_snow_records,
    _get_fresh_snow_record,
    _get_weather_forecast_at_altitude,
    _get_weather_forecast,
    _get_risk,
)
from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.sql.bra import DangerousSlopes, WindDirection, WeatherType

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def bra_xml_parsed() -> ET._Element:
    with open(
        os.path.join(CURRENT_DIR, "test_data/BRA.CHABLAIS.20190101142328.xml"), "rb"
    ) as xmlfile:
        return ET.parse(xmlfile)


class TestGetRisk:
    def test_get_risk_works(self, bra_xml_parsed):
        bra_id = uuid4()
        risks = _get_risk(bra_xml_parsed.find("//RISQUE"), bra_id)
        assert isinstance(risks, Generator)
        r = next(risks)
        assert r == {
            "r_record_id": bra_id,
            "r_altitude_limit": "<2200",
            "r_evolution": None,
            "r_risk": 1,
        }
        r = next(risks)
        assert r == {
            "r_record_id": bra_id,
            "r_altitude_limit": ">2200",
            "r_evolution": None,
            "r_risk": 2,
        }
        with pytest.raises(StopIteration):
            next(risks)

    def test_get_risk_only_one(self):
        bra_id = uuid4()
        xml = ET.fromstring(
            """
        <RISQUE RISQUE1="1" EVOLURISQUE1="" LOC1="" ALTITUDE="" RISQUE2="" EVOLURISQUE2=""
                    LOC2="" RISQUEMAXI="2" COMMENTAIRE=" "/>
        """
        )
        risks = _get_risk(xml, bra_id)
        assert isinstance(risks, Generator)
        r = next(risks)
        assert r == {
            "r_record_id": bra_id,
            "r_altitude_limit": None,
            "r_evolution": None,
            "r_risk": 1,
        }
        with pytest.raises(StopIteration):
            next(risks)


class TestGetMassifEntity:
    def test_no_massif(self, database):
        with connection_scope(database.engine) as con:
            with pytest.raises(ValueError) as e:
                _get_massif_id("CHABLAIS", con)
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
            "fsr_bra_record": bra_id,
            "fsr_date": datetime(2018, 12, 28, 00, 00, 00),
            "fsr_altitude": 1800,
            "sfr_massif_snowfall": 0,
            "fsr_second_massif_snowfall": -1,
        },
        {
            "fsr_bra_record": bra_id,
            "fsr_date": datetime(2018, 12, 29, 00, 00, 00),
            "fsr_altitude": 1800,
            "sfr_massif_snowfall": 0,
            "fsr_second_massif_snowfall": -1,
        },
        {
            "fsr_bra_record": bra_id,
            "fsr_date": datetime(2018, 12, 30, 00, 00, 00),
            "fsr_altitude": 1800,
            "sfr_massif_snowfall": 0,
            "fsr_second_massif_snowfall": -1,
        },
        {
            "fsr_bra_record": bra_id,
            "fsr_date": datetime(2018, 12, 31, 00, 00, 00),
            "fsr_altitude": 1800,
            "sfr_massif_snowfall": 0,
            "fsr_second_massif_snowfall": -1,
        },
        {
            "fsr_bra_record": bra_id,
            "fsr_date": datetime(2019, 1, 1, 00, 00, 00),
            "fsr_altitude": 1800,
            "sfr_massif_snowfall": 2,
            "fsr_second_massif_snowfall": -1,
        },
        {
            "fsr_bra_record": bra_id,
            "fsr_date": datetime(2019, 1, 2, 00, 00, 00),
            "fsr_altitude": 1800,
            "sfr_massif_snowfall": 3,
            "fsr_second_massif_snowfall": -1,
        },
    ]
    for i, fsr in enumerate(res):
        assert isinstance(fsr, dict)
        assert fsr == test_data[i]


class TestGetWeatherForecastAtAltitude:
    def test_get_weather_forecast_at_altitude_work(self, bra_xml_parsed):
        wf_id = uuid4()
        res = _get_weather_forecast_at_altitude(bra_xml_parsed, wf_id)
        assert isinstance(res, list)
        for i, data in enumerate(res):
            assert data["wfaa_wind_altitude"] == (2000, 2500)[i % 2]
            assert data["wfaa_wf_id"] == wf_id
            assert (
                data["wfaa_wind_direction"]
                == (
                    WindDirection.NE,
                    WindDirection.N,
                    WindDirection.NE,
                    WindDirection.N,
                    WindDirection.NE,
                    WindDirection.NE,
                )[i]
            )
            assert data["wfaa_wind_force"] == (20, 50, 40, 60, 60, 70)[i]


class TestGetWeatherForecast:
    def test_get_weather_forecast_work(self, bra_xml_parsed):
        bra_id = uuid4()
        res = _get_weather_forecast(bra_xml_parsed, bra_id)
        assert isinstance(res, dict)

        assert isinstance(res["weather_forecast"], list)
        assert len(res["weather_forecast"]) == 3

        expected_dict = [
            {
                "wf_bra_record": bra_id,
                "wf_expected_date": datetime(2019, 1, 2, 0, 0),
                "wf_weather_type": WeatherType(11),
                "wf_sea_of_clouds": -1,
                "wf_rain_snow_limit": 500,
                "wf_iso0": 800,
                "wf_iso_minus_10": 4000,
            },
            {
                "wf_bra_record": bra_id,
                "wf_expected_date": datetime(2019, 1, 2, 6, 0),
                "wf_weather_type": WeatherType(11),
                "wf_sea_of_clouds": -1,
                "wf_rain_snow_limit": 600,
                "wf_iso0": 800,
                "wf_iso_minus_10": 3400,
            },
            {
                "wf_bra_record": bra_id,
                "wf_expected_date": datetime(2019, 1, 2, 12, 0),
                "wf_weather_type": WeatherType(11),
                "wf_sea_of_clouds": -1,
                "wf_rain_snow_limit": 600,
                "wf_iso0": 900,
                "wf_iso_minus_10": 2900,
            },
        ]

        for index, wf in enumerate(res["weather_forecast"]):
            keys = expected_dict[index].keys()
            for k in keys:
                assert wf[k] == expected_dict[index][k]
        assert "weather_forecast_at_altitude" in res


class TestProcessXML:
    def _setup_test(self):
        # insert massifs chablais + zone.
        pass

    def test_process_xml_work(self, bra_xml_parsed, database):
        self._setup_test()
        with connection_scope(database.engine) as c:
            p = process_xml(c, bra_xml_parsed)
            assert isinstance(p, list)
