import os
from datetime import date, datetime
from uuid import uuid4, UUID

import pytest
import responses
from requests import HTTPError
from sqlalchemy.exc import IntegrityError

from nivo_api.cli import get_last_nivo_date, check_nivo_doesnt_exist, download_nivo
from nivo_api.cli.nivo_record_helper import (
    ArchiveNivoCss,
    NivoCsv,
    create_new_unknown_nivo_sensor_station,
)
from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.nivo import NivoSensorStation, NivoRecord
from nivo_api.settings import Config
from test.pytest_fixtures import setup_db

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestGetLastNivoDate:
    @responses.activate
    def test_wrong_date(self):
        """
        it should raise in case of wrongly formated date format.
        """
        responses.add(
            responses.GET, Config.METEO_FRANCE_LAST_NIVO_JS_URL, body="jour=20190;"
        )
        with pytest.raises(ValueError) as e:
            get_last_nivo_date()

    @responses.activate
    def test_wrong_file(self):
        """
        it should raise if the regex doesn't match
        """
        responses.add(
            responses.GET,
            Config.METEO_FRANCE_LAST_NIVO_JS_URL,
            body="THIS WILL NOT MATCH",
        )
        with pytest.raises(AttributeError) as e:
            get_last_nivo_date()
        assert str(e.value) == "'NoneType' object has no attribute 'group'"

    @responses.activate
    def test_file_fetch_error(self):
        responses.add(responses.GET, Config.METEO_FRANCE_LAST_NIVO_JS_URL, status=302)
        with pytest.raises(AssertionError) as e:
            get_last_nivo_date()
        assert str(e.value) == "Impossible to fetch last nivo data from meteofrance url"

    @responses.activate
    def test_date_ok(self):
        responses.add(
            responses.GET, Config.METEO_FRANCE_LAST_NIVO_JS_URL, body="jour=20190101;"
        )
        res = get_last_nivo_date()
        assert date(2019, 1, 1) == res


class TestCheckNivoDoesntExist:
    @setup_db()
    def test_check_nivo_doesnt_exist(self):
        r = check_nivo_doesnt_exist(date(2019, 1, 1))
        assert r is True

    def _inject_test_data(self):
        with connection_scope() as con:
            nss_id = uuid4()
            con.execute(
                NivoSensorStation.insert().values(
                    {
                        "nss_id": nss_id,
                        "nss_name": "test",
                        "nss_meteofrance_id": 1,
                        "the_geom": "SRID=4326;POINT(1 1 1)",
                    }
                )
            )
            con.execute(
                NivoRecord.insert().values(
                    {"nr_date": date(2019, 1, 1), "nr_nivo_sensor": nss_id}
                )
            )

    @setup_db()
    def test_check_nivo_exist(self):
        self._inject_test_data()
        r = check_nivo_doesnt_exist(date(2019, 1, 1))
        assert r is False


class TestDownloadNivo:
    @responses.activate
    def test_archive_download(self):
        url = f"{Config.METEO_FRANCE_NIVO_BASE_URL}/Archive/nivo.201701.csv.gz"
        with open(os.path.join(CURRENT_DIR, "test_data/nivo.201701.csv.gz"), "rb") as f:
            responses.add(
                responses.GET, url, body=f.read(), content_type="application/x-gzip"
            )
        r = download_nivo(date(2017, 1, 1), is_archive=True)
        assert isinstance(r, ArchiveNivoCss)
        assert r.nivo_date == date(2017, 1, 1)

    @responses.activate
    def test_recent_nivo_download(self):
        url = f"{Config.METEO_FRANCE_NIVO_BASE_URL}/nivo.20190812.csv"
        with open(os.path.join(CURRENT_DIR, "test_data/nivo.20190812.csv")) as f:
            responses.add(responses.GET, url, body=f.read(), content_type="text/plain")
        r = download_nivo(date(2019, 8, 12))
        assert isinstance(r, NivoCsv)
        assert r.nivo_date == date(2019, 8, 12)

    @responses.activate
    def test_download_fail(self):
        url = f"{Config.METEO_FRANCE_NIVO_BASE_URL}/nivo.20190812.csv"
        responses.add(responses.GET, url, status=503)
        with pytest.raises(HTTPError):
            download_nivo(date(2019, 8, 12))


class TestImportNivo:
    def test_import_nivo(self):
        raise NotImplementedError()

    def test_normalize_fail(self):
        raise NotImplementedError()

    def test_find_fk_fail(self):
        raise NotImplementedError()


class TestCreateNewUnknownNivoSensorStation:
    @setup_db()
    def test_create_new_unknown_nivo_sensor_station(self):
        with connection_scope() as con:
            r = create_new_unknown_nivo_sensor_station(10, con)
        assert isinstance(r.nss_id, UUID)

    @setup_db()
    def test_create_new_sensor_station_fail(self):
        """
        It should fail when two unknown station have the same name. non-idempotency is assumed (tech debt FTW)
        """
        with connection_scope() as con:
            with pytest.raises(IntegrityError):
                r = create_new_unknown_nivo_sensor_station(10, con)
                assert isinstance(r.nss_id, UUID)
                create_new_unknown_nivo_sensor_station(10, con)


def test_get_all_nivo_date():
    # need to mock FTP in order to do that.
    raise NotImplementedError()
