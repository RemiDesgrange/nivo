import logging
from typing import Generator, Dict, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from nivo_api.cli.bra_record_helper.miscellaneous import get_massif_geom
from nivo_api.core.db.models.sql.bra import MassifTable, DepartmentTable, ZoneTable

log = logging.getLogger(__name__)


def persist_bra(con: Connection, bra: List[Dict]):
    """
    This function is dumb, because it does not take care of the case when bra already exist
    """
    with con.begin():
        for entities in bra:
            for e, data in entities.items():
                # https://docs.sqlalchemy.org/en/13/core/tutorial.html#executing-multiple-statements
                if isinstance(data, Generator):
                    # execute is not capable of understanding a generator. But it understand list.
                    # behind the scene, the DBAPI `executemany` is called.
                    intermediate_data = [x for x in data if x]
                    data = intermediate_data
                # data can be null (generator yield None) then no need to execute
                if data:
                    con.execute(insert(e), data)


def persist_zone(con: Connection, zone: str) -> UUID:
    ins = insert(ZoneTable).values(z_name=zone)
    ins = ins.on_conflict_do_nothing(index_elements=["z_name"])
    con.execute(ins)
    res = select([ZoneTable.c.z_id]).where(ZoneTable.c.z_name == zone)
    return con.execute(res).first().z_id


def persist_department(con: Connection, name: str, number: str, zone: str) -> UUID:
    zone_id = persist_zone(con, zone)
    ins = insert(DepartmentTable).values(d_name=name, d_number=number, d_zone=zone_id)
    ins = ins.on_conflict_do_nothing(index_elements=["d_name"])
    con.execute(ins)
    res = select([DepartmentTable.c.d_id]).where(DepartmentTable.c.d_name == name)
    return con.execute(res).first().d_id


def persist_massif(con: Connection, name: str, department: Dict, zone: str) -> UUID:
    dept = persist_department(con, department["name"], department["number"], zone)
    try:
        geom = get_massif_geom(name)
        ins = insert(MassifTable).values(m_name=name, m_department=dept, the_geom=geom)
        ins = ins.on_conflict_do_nothing(index_elements=["m_name"])
        con.execute(ins)
        res = select([MassifTable.c.m_id]).where(MassifTable.c.m_name == name)
        return con.execute(res).first().m_id

    except ValueError as e:
        # get massif may fail with unknown massif.
        log.warning(e)
        raise e
