import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Generator
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
)

log = logging.getLogger(__name__)


def _get_risk_entity(risk: str, con: Connection) -> Optional[UUID]:
    if risk:
        res = con.execute(
            select([Risk.c.r_id]).where(Risk.c.r_number == int(risk))
        ).first()
        if not res:
            raise ValueError(f"Risk could not be found for level {risk} found in bra.")
        return res.r_id
    else:
        return None


def _get_massif_entity(massif: str, con: Connection) -> UUID:
    res = con.execute(
        select([Massif.c.bm_id]).where(Massif.c.bm_name == massif)
    ).first()
    if res:
        return res.bm_id
    else:
        raise ValueError(f"Cannot found massif {massif} in the db")


def _get_dangerous_slopes(xml: _Element) -> List["DangerousSlopes"]:
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


def _get_weather_forcast(
    bra_xml: _Element, bra_id: UUID
) -> Generator[Dict, None, None]:
    # quite complex
    yield {}


def _get_risk_forcast(bra_xml: _Element, bra_id: UUID) -> Generator[Dict, None, None]:
    class RiskEvolution(Enum):
        STABLE = 0
        UP = 0
        DOWN = -1

    for forcast in bra_xml.find("//TENDANCES").getchildren():
        evol = RiskEvolution(int(forcast.get("VALEUR")))
        evol = str(evol).split(".")[-1]
        yield {
            "rf_bra_record": bra_id,
            "rf_date": datetime.strptime(forcast.get("DATE"), "%Y-%m-%dT%H:%M:%S"),
            "rf_evolution": evol,
        }


def process_xml(con: Connection, bra_xml: ET._Element) -> List[Dict]:
    # split the XML in multiple entity object before merging them.
    bra_id = uuid4()

    return [
        {
            BraRecord: {
                "br_id": bra_id,
                "br_massif": _get_massif_entity(
                    bra_xml.find("//BULLETINS_NEIGE_AVALANCHE").get("MASSIF"), con
                ),
                "br_production_date": bra_xml.find("//BULLETINS_NEIGE_AVALANCHE").get(
                    "DATEDIFFUSION"
                ),
                "br_expiration_date": bra_xml.find("//DateValidite").text,
                "br_is_amended": bra_xml.find("//BULLETINS_NEIGE_AVALANCHE").get(
                    "AMENDEMENT"
                ),
                "br_max_risk": _get_risk_entity(
                    bra_xml.find("//RISQUE").get("RISQUEMAXI"), con
                ),
                "br_risk1": _get_risk_entity(
                    bra_xml.find("//RISQUE").get("RISQUE1"), con
                ),
                "br_risk1_altitude_limit": bra_xml.find("//RISQUE").get("LOC1"),
                "br_risk1_evolution": _get_risk_entity(
                    bra_xml.find("//RISQUE").get("EVOLURISQUE1"), con
                ),
                "br_risk2": _get_risk_entity(
                    bra_xml.find("//RISQUE").get("RISQUE2"), con
                ),
                "br_risk2_altitude_limit": bra_xml.find("//RISQUE").get("LOC2"),
                "br_risk2_evolution": _get_risk_entity(
                    bra_xml.find("//RISQUE").get("EVOLURISQUE2"), con
                ),
                "br_risk_comment": _get_risk_entity(
                    bra_xml.find("//RISQUE").get("COMMENTAIRE"), con
                ),
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
        {BraSnowRecord: _get_bra_snow_records(bra_xml, bra_id)},
        {BraFreshSnowRecord: _get_fresh_snow_record(bra_xml, bra_id)},
        {WeatherForcast: _get_weather_forcast(bra_xml, bra_id)},
        {RiskForcast: _get_risk_forcast(bra_xml, bra_id)},
    ]
