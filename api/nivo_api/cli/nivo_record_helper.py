import gzip
import io
import logging
import re
from abc import ABC
from csv import DictReader
from datetime import datetime, date
from ftplib import FTP
from typing import List, Dict

import requests
from sqlalchemy import select, exists, Date, cast
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection, RowProxy

from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.nivo import NivoRecord, NivoSensorStation
from nivo_api.settings import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# data quality is not the best stuiff at meteofrance.
SPECIAL_CHAR_TO_SET_TO_NONE =  ['mq', '/']

class ANivoCsv(ABC):
    """
    We have two case, the nivo is quite new and available as a csv, or old and archive. behavior vary between this
    two cases enough to justify two separate class
    """
    download_url: str
    nivo_date: date
    nivo_csv: DictReader
    cleaned_csv: List[Dict]

    def __init__(self, nivo_date: date, download_url: str = None):
        self.nivo_date = nivo_date
        self.cleaned_csv = list()

    def fetch_and_parse(self) -> DictReader:
        res = requests.get(self.download_url)
        assert res.status_code == 200
        self.nivo_csv = DictReader(io.StringIO(res.text), delimiter=';')
        return self.nivo_csv

    def normalize(self) -> List[Dict]:
        """
        Before importing to db, change invalid value
        """
        def remove_empty_column(line: Dict) -> Dict:
            for title, _ in line.items():
                if title == '':
                    line.pop(title)
            return line

        def remove_unvalid_int(line: Dict) -> Dict:
            # change invalid value that should be int but are string.
            for title, value in line.items():
                if value in SPECIAL_CHAR_TO_SET_TO_NONE:
                    line[title] = None
            return line

        def change_column_name(line: Dict) -> Dict:
            new_line = dict()
            for title, _ in line.items():
                new_line[f'nr_{title}'] = line[title]
            # special case : the foreign key
            new_line['nr_nivo_sensor'] = new_line.pop('nr_numer_sta')
            return new_line

        def parse_date(line: Dict) -> Dict:
            line['nr_date'] = datetime.strptime(line['nr_date'], '%Y%m%d%H%M%S')
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
            nivo_sensor = int(line['nr_nivo_sensor'])
            s = select([NivoSensorStation.c.nss_id]).where(
                NivoSensorStation.c.nss_meteofrance_id == nivo_sensor)
            res = con.execute(s).first()
            if res is None:
                logger.warning(f'No station have been found for id {nivo_sensor} creating an empty one.')
                res = create_new_unkown_nivo_sensor_station(nivo_sensor, con)
            line['nr_nivo_sensor'] = res.nss_id
            return line

        with connection_scope() as con:
            replaced_csv = list()
            for line in self.cleaned_csv:
                replaced_csv.append(replace_num_sta_by_column_name(line,con))
        self.cleaned_csv = replaced_csv
        return self.cleaned_csv


class NivoCsv(ANivoCsv):
    def __init__(self, nivo_date: date, download_url: str = None):
        super().__init__(nivo_date, download_url)
        download_date = date.strftime(nivo_date, "%Y%m%d")
        self.download_url = download_url or f"{Config.METEO_FRANCE_NIVO_BASE_URL}/nivo.{download_date}.csv"


class ArchiveNivoCss(ANivoCsv):
    def __init__(self, nivo_date: date, download_url: str = None):
        super().__init__(nivo_date, download_url)
        download_date = date.strftime(nivo_date, "%Y%m")
        self.download_url = download_url or f"{Config.METEO_FRANCE_NIVO_BASE_URL}/Archive/nivo.{download_date}.csv.gz"


def create_new_unkown_nivo_sensor_station(nivo_id: int, connection: Connection) -> RowProxy:
    ins = insert(NivoSensorStation).values(nss_name=f'UNKNOWN_{nivo_id}',
                                    nss_meteofrance_id=nivo_id,
                                    the_geom='SRID=4326;POINT(0 0 0)').returning(NivoSensorStation.c.nss_id)
    return connection.execute(ins).first()



def get_last_nivo_date() -> date:
    url = Config.METEO_FRANCE_LAST_NIVO_JS_URL
    res = requests.get(url)
    date_str = re.search('jour=(.*);', res.text).group(1)
    return datetime.strptime(date_str, '%Y%m%d').date()


def check_last_nivo_doesnt_exist(nivo_date: date) -> bool:
    with connection_scope() as con:
        s = exists([NivoRecord.c.nr_date]).where(cast(NivoRecord.c.nr_date, Date) == nivo_date)
        s = select([s.label('exists')])
        does_nivo_already_exist = con.execute(s).first().exists
        logger.info(f'does nivo for date {date} already exist : {does_nivo_already_exist}')
        return not does_nivo_already_exist


def download_nivo(nivo_date: date, is_archive=False) -> 'ANivoCsv':
    if is_archive:
        nivo_csv = ArchiveNivoCss(nivo_date)
    else:
        nivo_csv = NivoCsv(nivo_date)

    nivo_csv.fetch_and_parse()
    return nivo_csv


def import_nivo(csv_file: ANivoCsv):
    csv_file.normalize()
    csv_file.find_and_replace_foreign_key_value()
    with connection_scope() as con:
        with con.begin():
            ins = insert(NivoRecord).values(csv_file.cleaned_csv)#.on_conflict_do_nothing(index_elements=['nss_name'])
            con.execute(ins)



def get_all_nivo_date() -> List[Dict]:
    ftp = FTP(Config.METEO_FRANCE_FTP_DOMAIN_NAME)
    ftp.login()
    ftp.cwd('FDPMSP/Txt/Nivo/')
    nivo = ftp.nlst('nivo*.csv')
    def parse_filename(filename: str) -> Dict:
        date_str = re.search('nivo.(.*).csv', filename).group(1)
        return {
            'is_archive': False,
            'nivo_date': datetime.strptime(date_str, '%Y%m%d').date()
        }
    nivo_list = list(map(parse_filename, nivo))
    ftp.cwd('Archive')
    nivo = ftp.nlst('nivo*.csv.gz')

    def parse_filename_archived(filename: str) -> Dict:
        date_str = re.search('nivo.(.*).csv.gz', filename).group(1)
        return {
            'is_archive': True,
            'nivo_date': datetime.strptime(date_str, '%Y%m').date()
        }
    nivo_list_archived = list(map(parse_filename_archived, nivo))
    ftp.close()
    return nivo_list + nivo_list_archived