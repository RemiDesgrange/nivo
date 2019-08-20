import io
import logging
import os
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
    if res.status_code != 200:
        raise AssertionError(f"Bra list does not exist for {bra_date}")
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
    # meteofrance way of saying 404 is by redirecting you (302) to the 404 page, which is served with a 200 status...
    # so 302 means 404
    r = requests.get(url, allow_redirects=False)
    if r.status_code != 200:
        raise AssertionError(
            f"The bra for the massif {massif} at day {bra_date} doesn't exist, status: {r.status_code}"
        )
    # we could pass the url directly. But mocking in test would be more tricky. Using requests lib helps.
    return ET.parse(io.BytesIO(r.content))


def get_massif_geom(massif: str) -> WKBElement:
    """process to get the massifs geometries:
      * go on the meteofrance bra website
      * then get the html "area" element
     * then convert it to fake GeoJSON (wrong coordinates)
     * then open it in qgis.
     * Select *all* the geom of the layer.
     * rotate -90°
     * swap X and Y coordinates (with plugin)
     * use grass v.transform with various x, y scale and rotation until you get what you want.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    gj_file = os.path.join(current_dir, "../data/all_massifs.geojson")
    with open(gj_file) as fp:
        gj = geojson.load(fp)
    for obj in gj.features:
        if obj.properties["label"].upper() == massif.upper():
            return from_shape(shape(obj.geometry), 4326)
    else:
        raise ValueError(f"Massif {massif} geometry cannot be found.")
