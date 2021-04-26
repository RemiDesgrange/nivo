from dataclasses import dataclass
import io
import logging
import re
from abc import ABC
from csv import DictReader
from datetime import datetime, date, timedelta
from typing import List, Dict

import requests
from sqlalchemy import select, exists, Date, cast
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection, RowProxy
from nivo_api.core.db.models.sql.nivo import NivoRecordTable, SensorStationTable
from nivo_api.settings import Config

logger = logging.getLogger(__name__)

# data quality is not the best stuff at meteofrance.
SPECIAL_CHAR_TO_SET_TO_NONE = ["mq", "/"]


class ANivoCsv(ABC):
    """
    We have two case, the nivo is quite new and available as a csv, or old and archived. behavior vary between this
    two cases enough to justify two separate classes
    """

    download_url: str
    nivo_date: date
    nivo_csv: DictReader
    cleaned_csv: List[Dict]

    def __init__(
        self, nivo_date: "NivoDate", db_connection: Connection, download_url: str = None
    ):
        self.nivo_date = nivo_date.nivo_date
        self.cleaned_csv = []
        self.db_connection = db_connection

    def fetch_and_parse(self) -> DictReader:
        logger.debug(f"requests : {self.download_url}")
        res = requests.get(self.download_url, allow_redirects=False)
        if res.status_code == 302:
            raise requests.HTTPError("Cannot found Nivo record", response=res)
        res.raise_for_status()
        self.nivo_csv = DictReader(io.StringIO(res.text), delimiter=";")
        return self.nivo_csv

    def normalize(self) -> List[Dict]:
        """
        Before importing to db, change invalid value
        """

        def remove_empty_column(line: Dict) -> Dict:
            return {k: v for k, v in line.items() if k != ""}

        def remove_unvalid_int(line: Dict) -> Dict:
            # change invalid value that should be int but are string.
            for title, value in line.items():
                if value in SPECIAL_CHAR_TO_SET_TO_NONE:
                    line[title] = None
            return line

        def change_column_name(line: Dict) -> Dict:
            new_line = {f"nr_{title}": line[title] for title, _ in line.items()}
            # special case : the foreign key
            new_line["nr_nivo_sensor"] = new_line.pop("nr_numer_sta")
            return new_line

        def parse_date(line: Dict) -> Dict:
            line["nr_date"] = datetime.strptime(line["nr_date"], "%Y%m%d%H%M%S")
            return line

        filtered_csv = map(remove_empty_column, self.nivo_csv)
        filtered_csv = map(remove_unvalid_int, filtered_csv)
        filtered_csv = map(change_column_name, filtered_csv)
        filtered_csv = map(parse_date, filtered_csv)
        self.cleaned_csv = list(filtered_csv)
        return self.cleaned_csv

    def find_and_replace_foreign_key_value(self) -> List[Dict]:
        def replace_num_sta_by_column_name(line: Dict, con: Connection) -> Dict:
            """
            You have to know that some station have no id (yes...)
            """
            nivo_sensor = int(line["nr_nivo_sensor"])
            s = select([SensorStationTable.c.nss_id]).where(
                SensorStationTable.c.nss_meteofrance_id == nivo_sensor
            )
            res = con.execute(s).first()
            if res is None:
                logger.warning(
                    f"No station have been found for id {nivo_sensor} creating an empty one."
                )
                res = create_new_unknown_nivo_sensor_station(nivo_sensor, con)
            line["nr_nivo_sensor"] = res.nss_id
            return line

        replaced_csv = list()
        for line in self.cleaned_csv:
            replaced_csv.append(
                replace_num_sta_by_column_name(line, self.db_connection)
            )
        self.cleaned_csv = replaced_csv
        return self.cleaned_csv


class NivoCsv(ANivoCsv):
    def __init__(
        self, nivo_date: "NivoDate", db_connection: Connection, download_url: str = None
    ):
        super().__init__(nivo_date, db_connection, download_url)
        download_date = date.strftime(nivo_date.nivo_date, "%Y%m%d")
        self.download_url = (
            download_url
            or f"{Config.METEO_FRANCE_NIVO_BASE_URL}/nivo.{download_date}.csv"
        )


class ArchiveNivoCss(ANivoCsv):
    def __init__(
        self, nivo_date: "NivoDate", db_connection: Connection, download_url: str = None
    ):
        super().__init__(nivo_date, db_connection, download_url)
        download_date = date.strftime(nivo_date.nivo_date, "%Y%m")
        self.download_url = (
            download_url
            or f"{Config.METEO_FRANCE_NIVO_BASE_URL}/Archive/nivo.{download_date}.csv.gz"
        )


def create_new_unknown_nivo_sensor_station(
    nivo_id: int, connection: Connection
) -> RowProxy:
    ins = (
        insert(SensorStationTable)
        .values(
            nss_name=f"UNKNOWN_{nivo_id}",
            nss_meteofrance_id=nivo_id,
            the_geom="SRID=4326;POINT(0 0 0)",
        )
        .returning(SensorStationTable.c.nss_id)
    )
    return connection.execute(ins).first()


def get_last_nivo_date() -> "NivoDate":
    url = Config.METEO_FRANCE_LAST_NIVO_JS_URL
    res = requests.get(url, allow_redirects=False)
    if res.status_code != 200:
        raise AssertionError("Impossible to fetch last nivo data from meteofrance url")
    date_str = re.search("jour=(.*);", res.text).group(1)  # type: ignore
    return NivoDate(
        is_archive=False, nivo_date=datetime.strptime(date_str, "%Y%m%d").date()
    )


def check_nivo_doesnt_exist(con: Connection, nivo_date: date) -> bool:
    s = exists([NivoRecordTable.c.nr_date]).where(
        cast(NivoRecordTable.c.nr_date, Date) == nivo_date
    )
    s = select([s.label("exists")])
    does_nivo_already_exist = con.execute(s).first().exists
    logger.debug(
        f"does nivo for date {nivo_date.strftime('%d-%m-%Y')} already exist : {does_nivo_already_exist}"
    )
    return not does_nivo_already_exist


def download_nivo(nivo_date: "NivoDate", db_connection: Connection) -> "ANivoCsv":
    nivo_csv: ANivoCsv
    if nivo_date.is_archive:
        nivo_csv = ArchiveNivoCss(nivo_date, db_connection)
    else:
        nivo_csv = NivoCsv(nivo_date, db_connection)

    nivo_csv.fetch_and_parse()
    return nivo_csv


def import_nivo(con: Connection, csv_file: ANivoCsv) -> None:
    csv_file.normalize()
    csv_file.find_and_replace_foreign_key_value()
    with con.begin():
        ins = insert(NivoRecordTable).values(
            csv_file.cleaned_csv
        )  # .on_conflict_do_nothing(index_elements=['nss_name'])
        con.execute(ins)


@dataclass
class NivoDate:
    is_archive: bool
    nivo_date: date


def get_all_nivo_date() -> List["NivoDate"]:
    """
    create nivo date to downloads programmaticaly
    """

    def generate_archive_date_range():
        first_archived_record = date(year=2010, month=12, day=1)
        last_archived_record = date.today() - timedelta(days=15)
        total_months = lambda dt: dt.month + 12 * dt.year
        months_list = []
        for tot_m in range(
            total_months(first_archived_record) - 1, total_months(last_archived_record)
        ):
            y, m = divmod(tot_m, 12)
            months_list.append(NivoDate(is_archive=True, nivo_date=date(y, m + 1, 1)))
        return months_list

    nivo_list_archived = generate_archive_date_range()
    start_date = date.today() - timedelta(days=15)
    nivo_list = [
        NivoDate(is_archive=False, nivo_date=(date.today() - timedelta(days=x)))
        for x in range(0, (date.today() - start_date).days + 1)
    ]
    return nivo_list_archived + nivo_list
