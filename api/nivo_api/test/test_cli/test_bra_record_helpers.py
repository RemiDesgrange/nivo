import json
import os
from datetime import datetime

from lxml import etree
import pytest
import responses
from freezegun import freeze_time

from nivo_api.cli.bra_record_helper import get_last_bra_date, get_bra_xml
from nivo_api.settings import Config

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


# make it so it doesn't exist
# bra are served from december to april/may
@freeze_time("2019-09-10")
def test_get_last_bra_date_fail():
    with pytest.raises(AssertionError) as e:
        get_last_bra_date()

    assert str(e.value) == "Bra list does not exist for 2019-09-10"


@responses.activate
@freeze_time("2019-01-01")
def test_get_last_date_work():
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
def test_get_last_date_malformed_json():
    with open(os.path.join(CURRENT_DIR, 'bra.malformed.json')) as bra_json:
        responses.add(responses.GET, Config.BRA_BASE_URL + f'/bra.20190101.json',
                      json=json.load(bra_json))
    with pytest.raises(ValueError) as e:
        get_last_bra_date()
    assert str(e.value) == 'JSON provided is malformed. Cannot parse'


@responses.activate
def test_get_bra_xml_fail():
    responses.add(responses.GET, Config.BRA_BASE_URL + f'/BRA.CHABLAIS.20190101142328.xml',
                  body='bla bla',
                  status=302)
    with pytest.raises(AssertionError) as e:
        get_bra_xml('CHABLAIS', datetime.strptime('20190101142328', '%Y%m%d%H%M%S'))
    assert str(e.value) == "The bra for the massif CHABLAIS at day 2019-01-01 14:23:28 doesn't exist"


@responses.activate
def test_get_bra_xml_work():
    with open(os.path.join(CURRENT_DIR, 'BRA.CHABLAIS.20190101142328.xml')) as bra_xml:
        responses.add(responses.GET, Config.BRA_BASE_URL + f'/BRA.CHABLAIS.20190101142328.xml',
                      body=bra_xml.read(),
                      content_type='text/xml')

        res = get_bra_xml('CHABLAIS', datetime.strptime('20190101142328', '%Y%m%d%H%M%S'))
    assert isinstance(res, etree._Element)


