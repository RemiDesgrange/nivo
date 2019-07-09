import logging
from datetime import datetime, date

from json import JSONDecodeError
from typing import Dict, Tuple

import geojson
import requests
import lxml.etree as ET
from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from nivo_api.settings import Config

log = logging.getLogger(__name__)


def get_bra_date(bra_date: date) -> Dict[str, datetime]:
    """
    return, for all massifs, the exact date for bra. in order to download it.
    """
    bra_date_str = bra_date.strftime("%Y%m%d")
    res = requests.get(
        Config.BRA_BASE_URL + f"/bra.{bra_date_str}.json", allow_redirects=False
    )
    assert res.status_code == 200, f"Bra list does not exist for {bra_date}"
    try:
        massifs_json = res.json()

        def merge_massifs(massif: Dict) -> Tuple[str, datetime]:
            name = massif["massif"]
            bra_date = datetime.strptime(massif["heures"].pop(), "%Y%m%d%H%M%S")
            return (name, bra_date)

        massif_dict = dict(map(merge_massifs, massifs_json))
        return massif_dict
    except JSONDecodeError as e:
        log.critical("Decoding of the json failed, I probably doesn't exist")
        raise e
    except (KeyError, TypeError):
        raise ValueError("JSON provided is malformed. Cannot parse")


def get_last_bra_date() -> Dict[str, datetime]:
    """

    :return: a simple dict with the name of the massif as key and the date as value
    """
    today = datetime.now().date()
    return get_bra_date(today)


def get_bra_xml(massif: str, bra_date: datetime) -> ET:
    bra_date_str = bra_date.strftime("%Y%m%d%H%M%S")
    url = Config.BRA_BASE_URL + f"/BRA.{massif}.{bra_date_str}.xml"
    r = requests.get(url, allow_redirects=False)
    assert (
        r.status_code == 200
    ), f"The bra for the massif {massif} at day {bra_date} doesn't exist"
    return ET.parse(r.content)


def fetch_massif_geom_from_opendata(massif: str) -> WKBElement:
    # go on the meteofrance bra website
    # then get the html "area" element
    # then convert it to GeoJSON
    raise NotImplemented()


def fetch_department_geom_from_opendata(dept: str, dept_nb: str) -> WKBElement:
    dept = dept.lower()
    raw_dept = requests.get(
        f"https://france-geojson.gregoiredavid.fr/repo/departements/{dept_nb}-{dept}/departement-{dept_nb}-{dept}.geojson"
    )
    assert (
        raw_dept.status_code == 200
    ), f"Something went wrong with department geometry fetching from the internet, status : {raw_dept.status_code}"
    gj = geojson.loads(raw_dept.text)
    return from_shape(shape(gj.geometry), 4326)

