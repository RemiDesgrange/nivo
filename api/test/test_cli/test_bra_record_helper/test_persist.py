from uuid import UUID


from sqlalchemy import select, bindparam

from nivo_api.cli.bra_record_helper.persist import persist_zone, persist_massif
from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.sql.bra import ZoneTable, DepartmentTable, MassifTable

from test.pytest_fixtures import database


class TestPersistZone:
    def test_insert_zone(self, database):
        with connection_scope(database.engine) as con:
            r = persist_zone(con, "this_is_a_test")
            assert isinstance(r, UUID)

    def test_multi_insert(self, database):
        with connection_scope(database.engine) as con:
            uuid_list = [persist_zone(con, "this_is_a_test") for _ in range(5)]
            for x in uuid_list:
                assert isinstance(x, UUID)
                assert all(x == uuid_list[0] for x in uuid_list)


class TestPersistMassif:
    def test_massif(self, database):
        with connection_scope(database.engine) as con:
            r = persist_massif(
                con,
                "CHABLAIS",
                {"name": "Haute-savoie", "number": "74"},
                "Alpes du Nord",
            )
            assert isinstance(r, UUID)

    def test_multi_massif(self, database):
        with connection_scope(database.engine) as con:
            r1 = persist_massif(
                con,
                "CHABLAIS",
                {"name": "Haute-savoie", "number": "74"},
                "Alpes du Nord",
            )
            r2 = persist_massif(
                con,
                "MONT-BLANC",
                {"name": "Haute-savoie", "number": "74"},
                "Alpes du Nord",
            )
            assert isinstance(r1, UUID)
            assert isinstance(r2, UUID)
            req = (
                select([ZoneTable.c.z_id, DepartmentTable.c.d_id])
                .select_from(ZoneTable.join(DepartmentTable).join(MassifTable))
                .where(MassifTable.c.m_id == bindparam("massif"))
            )
            id1 = con.execute(req, massif=r1).first()
            id2 = con.execute(req, massif=r2).first()
            assert id1.z_id == id2.z_id
            assert id1.d_id == id2.d_id


class TestPersistBra:
    def test_persist_bra(self):
        raise NotImplementedError()
