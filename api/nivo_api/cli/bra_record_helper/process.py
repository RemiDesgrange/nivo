"""
Process xml pieces by pieces to dict ready to be inserted in DB.
"""
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Generator, Any
from uuid import UUID, uuid4

import lxml.etree as ET
from lxml.etree import _Element
from sqlalchemy import select
from sqlalchemy.engine import Connection

from nivo_api.core.db.models.bra import (
    Risk,
    Massif,
    DangerousSlopes,
    BraRecord,
    BraSnowRecord,
    BraFreshSnowRecord,
    WeatherForcast,
    RiskForcast,
    WindDirection,
    WeatherType,
    RiskEvolution,
    WeatherForcastAtAltitude,
)

log = logging.getLogger(__name__)


def _transform_or_none(data: Any, t: Any) -> Optional[Any]:
    """
    It does *not* fail silently
    """
    if data:
        return t(data)
    return None


def _get_risk(bra_xml, bra_id) -> Generator[Dict, None, None]:
    """
    It could exist 2 risk, one belong a certain altitude, and one upper. If altitude is set, then below this altitude
    you have a risk and above you have another risk.
    """
    if bra_xml.tag != "RISQUE" and not isinstance(bra_xml, _Element):
        raise ValueError(
            f"Need to pass RISQUE xml element to this function found : {bra_xml.tag}"
        )
    yield {
        "r_record_id": bra_id,
        "r_altitude_limit": _transform_or_none(bra_xml.get("LOC1"), str),
        "r_evolution": _transform_or_none(bra_xml.get("EVOLURISQUE1"), int),
        "r_risk": _transform_or_none(bra_xml.get("RISQUE1"), int),
    }
    if bra_xml.get("ALTITUDE"):
        yield {
            "r_record_id": bra_id,
            "r_altitude_limit": bra_xml.get("LOC2"),
            "r_evolution": _transform_or_none(bra_xml.get("EVOLURISQUE2"), int),
            "r_risk": _transform_or_none(bra_xml.get("RISQUE2"), int),
        }


def _get_massif_id(massif: str, con: Connection) -> UUID:
    res = con.execute(
        select([Massif.c.bm_id]).where(Massif.c.bm_name == massif)
    ).first()
    if res:
        return res.bm_id
    else:
        raise ValueError(f"Cannot found massif {massif} in the db")


def _get_dangerous_slopes(xml: _Element) -> List[DangerousSlopes]:
    dangerous_slopes_list = list()
    for k, v in xml.find("//PENTE").items():
        if v == "true" and k != "COMMENTAIRE":
            dangerous_slopes_list.append(DangerousSlopes(k))
    return dangerous_slopes_list


def _get_bra_snow_records(
    bra_xml: _Element, bra_id: UUID
) -> Generator[Dict, None, None]:
    for x in bra_xml.find("//ENNEIGEMENT").getchildren():
        if x.tag == "NIVEAU":
            yield {
                "s_bra_record": bra_id,
                "s_altitude": int(x.get("ALTI")),
                "s_snow_quantity_cm_north": int(x.get("N")),
                "s_snow_quantity_cm_south": int(x.get("S")),
            }


def _get_fresh_snow_record(bra_xml: _Element, bra_id) -> Generator[Dict, None, None]:
    for record in bra_xml.find("//NEIGEFRAICHE").getchildren():
        if record.tag == "NEIGE24H":
            yield {
                "bfsr_bra_record": bra_id,
                "bfsr_date": datetime.strptime(record.get("DATE"), "%Y-%m-%dT%H:%M:%S"),
                "bfsr_altitude": int(bra_xml.find("//NEIGEFRAICHE").get("ALTITUDESS")),
                "bsfr_massif_snowfall": int(record.get("SS241")),
                "bfsr_second_massif_snowfall": int(record.get("SS242")),
            }


def _get_weather_forcast_at_altitude(
    bra_xml: _Element, wf_id: UUID
) -> Generator[Dict, None, None]:
    """
    for exach altitude of the forcast return the wind direction and force
    """
    altitudes = [int(v) for _, v in bra_xml.find("//METEO").attrib.items()]
    for record in bra_xml.find("//METEO").getchildren():
        if record.tag == "ECHEANCE":
            for alt_index, alt in enumerate(altitudes, 1):
                wind_dir = record.get(f"DD{alt_index}")
                win_force = record.get(f"FF{alt_index}")
                if not wind_dir:
                    raise ValueError(f"Cannot found value for index {alt_index}")
                yield {
                    "wfaa_wf_id": wf_id,
                    "wfaa_wind_altitude": alt,
                    "wfaa_wind_direction": WindDirection(wind_dir),
                    "wfaa_wind_force": int(win_force),
                }


def _get_weather_forcast(
    bra_xml: _Element, bra_id: UUID, wf_id: UUID
) -> Generator[Dict, None, None]:
    for record in bra_xml.find("//METEO").getchildren():
        if record.tag == "ECHEANCE":
            yield {
                "wf_id": wf_id,
                "wf_bra_record": bra_id,
                "wf_expected_date": datetime.strptime(
                    record.get("DATE"), "%Y-%m-%dT%H:%M:%S"
                ),
                "wf_weather_type": WeatherType(int(record.get("TEMPSSENSIBLE"))),
                "wf_sea_of_clouds": int(record.get("MERNUAGES")),
                "wf_rain_snow_limit": int(record.get("PLUIENEIGE")),
                "wf_iso0": int(record.get("ISO0")),
                "wf_iso_minus_10": int(record.get("ISO-10")),
            }


def _get_risk_forcast(bra_xml: _Element, bra_id: UUID) -> Generator[Dict, None, None]:

    for forcast in bra_xml.find("//TENDANCES").getchildren():
        evol = RiskEvolution(int(forcast.get("VALEUR")))
        evol = str(evol).split(".")[
            -1
        ]  # TODO need to move RiskEvolution Enum to models, since sqlalchemy suport native enum !
        yield {
            "rf_bra_record": bra_id,
            "rf_date": datetime.strptime(forcast.get("DATE"), "%Y-%m-%dT%H:%M:%S"),
            "rf_evolution": evol,
        }


def process_xml(con: Connection, bra_xml: ET._Element) -> List[Dict]:
    # split the XML in multiple entity object before merging them.
    bra_id = uuid4()
    # weather forcast id
    wf_id = uuid4()
    return [
        {
            BraRecord: {
                "br_id": bra_id,
                "br_massif": _get_massif_id(
                    bra_xml.find("//BULLETINS_NEIGE_AVALANCHE").get("MASSIF"), con
                ),
                "br_production_date": bra_xml.find("//BULLETINS_NEIGE_AVALANCHE").get(
                    "DATEDIFFUSION"
                ),
                "br_expiration_date": bra_xml.find("//DateValidite").text,
                "br_is_amended": bra_xml.find("//BULLETINS_NEIGE_AVALANCHE").get(
                    "AMENDEMENT"
                ),
                "br_max_risk": bra_xml.find("//RISQUE").get("RISQUEMAXI"),
                "br_risk_comment": bra_xml.find("//RISQUE").get("COMMENTAIRE"),
                "br_dangerous_slopes": _get_dangerous_slopes(bra_xml),
                "br_dangerous_slopes_comment": bra_xml.find("//PENTE").get(
                    "COMMENTAIRE"
                ),
                "br_opinion": bra_xml.find(""),
                "br_snow_quality": bra_xml.find("//QUALITE/TEXTE").text,
                "br_snow_stability": bra_xml.find("//STABILITE/TEXTE").text,
                "br_last_snowfall_date": "",
                "br_snowlimit_south": bra_xml.find("//ENNEIGEMENT").get("LimiteSud"),
                "br_snowlimit_north": bra_xml.find("//ENNEIGEMENT").get("LimiteNord"),
            }
        },
        {Risk: _get_risk(bra_xml.find("//RISQUE"), bra_id)},
        {BraSnowRecord: _get_bra_snow_records(bra_xml, bra_id)},
        {BraFreshSnowRecord: _get_fresh_snow_record(bra_xml, bra_id)},
        {WeatherForcast: _get_weather_forcast(bra_xml, bra_id, wf_id)},
        {WeatherForcastAtAltitude: _get_weather_forcast_at_altitude(bra_xml, wf_id)},
        {RiskForcast: _get_risk_forcast(bra_xml, bra_id)},
    ]
