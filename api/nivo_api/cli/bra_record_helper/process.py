"""
Process xml pieces by pieces to dict ready to be inserted in DB.
"""
import logging
from datetime import datetime
from distutils.util import strtobool
from typing import Dict, List, Optional, Generator, Any
from uuid import UUID, uuid4

import lxml.etree as ET
from lxml.etree import _Element
from sqlalchemy import select
from sqlalchemy.engine import Connection

from nivo_api.core.db.models.sql.bra import (
    RiskTable,
    MassifTable,
    DangerousSlopes,
    BraRecordTable,
    SnowRecordTable,
    FreshSnowRecordTable,
    WeatherForcastTable,
    RiskForcastTable,
    WindDirection,
    WeatherType,
    RiskEvolution,
    WeatherForcastAtAltitudeTable,
)

log = logging.getLogger(__name__)


def _transform_or_none(data: Any, t: Any) -> Optional[Any]:
    """
    It does *not* fail silently
    """
    if data:
        try:
            return t(data)
        except Exception as e:
            log.debug(f"Failed to convert {data} to {type(t)}, returning None")
            log.debug(e)
    return None


def _get_bra_record(bra_xml: _Element, bra_id: UUID, con: Connection) -> Dict:
    return {
        "br_id": bra_id,
        "br_massif": _get_massif_id(
            bra_xml.find("//BULLETINS_NEIGE_AVALANCHE").get("MASSIF"), con
        ),
        "br_production_date": bra_xml.find("//BULLETINS_NEIGE_AVALANCHE").get(
            "DATEDIFFUSION"
        ),
        "br_expiration_date": bra_xml.find("//DateValidite").text,
        "br_is_amended": strtobool(
            bra_xml.find("//BULLETINS_NEIGE_AVALANCHE").get("AMENDEMENT")
        ),
        "br_max_risk": _transform_or_none(
            bra_xml.find("//RISQUE").get("RISQUEMAXI"), int
        ),
        "br_risk_comment": bra_xml.find("//RISQUE").get("COMMENTAIRE"),
        "br_dangerous_slopes": _get_dangerous_slopes(bra_xml),
        "br_dangerous_slopes_comment": bra_xml.find("//PENTE").get("COMMENTAIRE"),
        "br_opinion": bra_xml.find("//AVIS").text,
        "br_snow_quality": bra_xml.find("//QUALITE/TEXTE").text,
        "br_snow_stability": bra_xml.find("//STABILITE/TEXTE").text,
        "br_last_snowfall_date": None,  # TODO !
        "br_snowlimit_south": bra_xml.find("//ENNEIGEMENT").get("LimiteSud"),
        "br_snowlimit_north": bra_xml.find("//ENNEIGEMENT").get("LimiteNord"),
        "br_raw_xml": bra_xml,
    }


def _get_risk(
    bra_xml: _Element, bra_id: UUID
) -> Generator[Optional[Dict[Any, Any]], None, None]:
    """
    It could exist 2 risk, one belong a certain altitude, and one upper. If altitude is set, then below this altitude
    you have a risk and above you have another risk.
    """
    if bra_xml.tag != "RISQUE" and not isinstance(bra_xml, _Element):
        raise ValueError(
            f"Need to pass RISQUE xml element to this function found : {bra_xml.tag}"
        )
    risk = {
        "r_record_id": bra_id,
        "r_altitude_limit": _transform_or_none(bra_xml.get("LOC1"), str),
        "r_evolution": _transform_or_none(bra_xml.get("EVOLURISQUE1"), int),
        "r_risk": _transform_or_none(bra_xml.get("RISQUE1"), int),
    }
    # check for inconsistencies, for example -1 value in risk
    if risk["r_risk"] == -1:
        yield None
    else:
        yield risk

    if bra_xml.get("ALTITUDE") and bra_xml.get("ALTITUDE") != "-1":
        yield {
            "r_record_id": bra_id,
            "r_altitude_limit": bra_xml.get("LOC2"),
            "r_evolution": _transform_or_none(bra_xml.get("EVOLURISQUE2"), int),
            "r_risk": _transform_or_none(bra_xml.get("RISQUE2"), int),
        }


def _get_massif_id(massif: str, con: Connection) -> UUID:
    # this is a special case with Orlu StBarthelemy massif bra. The amount of special case code is acceptable for me
    massif_cleaned = massif.replace(" ", "_")
    res = con.execute(
        select([MassifTable.c.m_id]).where(MassifTable.c.m_name == massif_cleaned)
    ).first()
    if res:
        return res.m_id
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
                "fsr_bra_record": bra_id,
                "fsr_date": datetime.strptime(record.get("DATE"), "%Y-%m-%dT%H:%M:%S"),
                "fsr_altitude": int(bra_xml.find("//NEIGEFRAICHE").get("ALTITUDESS")),
                "sfr_massif_snowfall": int(record.get("SS241")),
                "fsr_second_massif_snowfall": int(record.get("SS242")),
            }


def _get_weather_forcast_at_altitude(bra_xml: _Element, wf_id: UUID) -> List:
    """
    for exach altitude of the forcast return the wind direction and force
    """
    altitudes = [int(v) for _, v in bra_xml.find("//METEO").attrib.items()]
    wfaa_final = list()
    for record in bra_xml.find("//METEO").getchildren():
        if record.tag == "ECHEANCE":
            for alt_index, alt in enumerate(altitudes, 1):
                wind_dir = record.get(f"DD{alt_index}")
                wind_force = record.get(f"FF{alt_index}")
                if wind_dir:  # sometime wind_dir is empty ¯\_(ツ)_/¯
                    wfaa_final.append(
                        {
                            "wfaa_wf_id": wf_id,
                            "wfaa_wind_altitude": alt,
                            "wfaa_wind_direction": WindDirection(wind_dir),
                            "wfaa_wind_force": int(wind_force),
                        }
                    )
    return wfaa_final


def _get_weather_forcast(bra_xml: _Element, bra_id: UUID) -> Dict:
    weather_forcasts = list()
    weather_forcasts_at_altitude = list()
    for record in bra_xml.find("//METEO").getchildren():
        if record.tag == "ECHEANCE":
            wf_id = uuid4()
            weather_forcasts.append(
                {
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
            )
            weather_forcasts_at_altitude += _get_weather_forcast_at_altitude(
                bra_xml, wf_id
            )

    return {
        "weather_forcast": weather_forcasts,
        "weather_forcast_at_altitude": weather_forcasts_at_altitude,
    }


def _get_risk_forcast(bra_xml: _Element, bra_id: UUID) -> Generator[Dict, None, None]:
    for forcast in bra_xml.find("//TENDANCES").getchildren():
        evol = RiskEvolution(int(forcast.get("VALEUR")))
        evol_str = str(evol).split(".")[-1]
        yield {
            "rf_bra_record": bra_id,
            "rf_date": datetime.strptime(forcast.get("DATE"), "%Y-%m-%dT%H:%M:%S"),
            "rf_evolution": evol_str,
        }


def process_xml(con: Connection, bra_xml: ET._Element) -> List[Dict]:
    # split the XML in multiple entity object before merging them.
    bra_id = uuid4()
    weather_forcasts = _get_weather_forcast(bra_xml, bra_id)
    return [
        {BraRecordTable: _get_bra_record(bra_xml, bra_id, con)},
        {RiskTable: _get_risk(bra_xml.find("//RISQUE"), bra_id)},
        {SnowRecordTable: _get_bra_snow_records(bra_xml, bra_id)},
        {FreshSnowRecordTable: _get_fresh_snow_record(bra_xml, bra_id)},
        {WeatherForcastTable: weather_forcasts["weather_forcast"]},
        {
            WeatherForcastAtAltitudeTable: weather_forcasts[
                "weather_forcast_at_altitude"
            ]
        },
        {RiskForcastTable: _get_risk_forcast(bra_xml, bra_id)},
    ]
