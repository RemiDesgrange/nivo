import logging
from typing import Generator, Dict, List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from nivo_api.cli.bra_record_helper.miscellaneous import get_massif_geom
from nivo_api.core.db.models.bra import Massif, Department, Zone

log = logging.getLogger(__name__)


def persist_bra(con: Connection, bra: List[Dict]):
    for entities in bra:
        with con.begin():
            for e, data in entities.items():
                ins = insert(e).values(**data)
                con.execute(ins)


def persist_zone(con: Connection, zone: str) -> UUID:
    ins = insert(Zone).values(bz_name=zone)
    ins = ins.on_conflict_do_nothing(index_elements=["bz_name"])
    con.execute(ins)
    res = select([Zone.c.bz_id]).where(Zone.c.bz_name == zone)
    return con.execute(res).first().bz_id


def persist_department(con: Connection, name: str, number: str, zone: str) -> UUID:
    zone_id = persist_zone(con, zone)
    ins = insert(Department).values(bd_name=name, bd_number=number, bd_zone=zone_id)
    ins = ins.on_conflict_do_nothing(index_elements=["bd_name"])
    con.execute(ins)
    res = select([Department.c.bd_id]).where(Department.c.bd_name == name)
    return con.execute(res).first().bd_id


def persist_massif(con: Connection, name: str, department: Dict, zone: str) -> UUID:
    dept = persist_department(con, department["name"], department["number"], zone)
    try:
        geom = get_massif_geom(name)
        ins = insert(Massif).values(bm_name=name, bm_department=dept, the_geom=geom)
        ins = ins.on_conflict_do_nothing(index_elements=["bm_name"])
        con.execute(ins)
        res = select([Massif.c.bm_id]).where(Massif.c.bm_name == name)
        return con.execute(res).first().bm_id

    except ValueError as e:
        # get massif may fail with unknown massif.
        log.warning(e)
        raise e
