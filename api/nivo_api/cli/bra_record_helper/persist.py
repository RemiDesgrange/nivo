import logging
from typing import Generator, Dict
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from nivo_api.cli.bra_record_helper.miscellaneous import fetch_massif_geom_from_opendata, \
    fetch_department_geom_from_opendata, build_zone_from_department_geom
from nivo_api.core.db.models.bra import Massif, Department

log = logging.getLogger(__name__)


def _get_entity(bra_generator):
    x = next(bra_generator)
    if isinstance(x, Generator):
        x = _get_entity(x)
    return x


def persist_bra(con: Connection, bra_generator: Generator):
    for entity in _get_entity(bra_generator):
        pass  # TODO


def persist_department(con: Connection, name: str, number: int) -> UUID:
    geom = fetch_department_geom_from_opendata(name)
    ins = insert(Department).values(bd_name=name, bd_number=number, the_geom=geom)
    ins = ins.on_conflict_do_update(
        index_elements=['bd_name'],
        set_={'bd_id': ins.excluded.bd_id}
    ).returning(Department.c.bd_id)
    return con.execute(ins).first().bd_id


def persist_zone(con: Connection, zone: str) -> UUID:
    geom = build_zone_from_department_geom(zone)
    ins = insert(Department).values(bz_name=zone, the_geom=geom)
    ins = ins.on_conflict_do_update(
        index_elements=['bz_name'],
        set_={'bz_id': ins.excluded.bz_id}
    ).returning(Department.c.bz_id)
    return con.execute(ins).first().bz_id

def persist_massif(con: Connection, name: str, departement: Dict, zone: str) -> UUID:
    dept = persist_department(con, departement['name'], departement['number'])
    zone = persist_zone(con, zone)
    geom = fetch_massif_geom_from_opendata(name)
    ins = insert(Massif).values(bm_name=name, bm_department=dept, bm_zone=zone, the_geom=geom)
    ins = ins.on_conflict_do_update(
        index_elements=['bm_name'],
        set_={'bm_id': ins.excluded.bm_id}
    ).returning(Massif.c.bm_id)
    return con.execute(ins).first().bm_id
