from contextlib import contextmanager


from click.testing import CliRunner
from sqlalchemy import text
from uuid import UUID
from sqlalchemy.engine import RowProxy

from nivo_api.cli import init_db
from nivo_api.cli.nivo_record_helper import create_new_unkown_nivo_sensor_station
from nivo_api.core.db.connection import db_engine, connection_scope
# populate metadata
from nivo_api.core.db.models.nivo import  metadata


@contextmanager
def setup_db():
    metadata.drop_all(db_engine)
    metadata.create_all(db_engine)
    yield
    metadata.drop_all(db_engine)

class TestInitDb():
    def test_init_db(self):
        metadata.drop_all(db_engine)
        runner = CliRunner()
        result = runner.invoke(init_db)
        assert result.exit_code == 0
        with connection_scope() as con:
            for table in metadata.sorted_tables:
                schema = metadata.schema if metadata.schema else 'public'
                table = table.name
                res = con.execute(text(f'''SELECT to_regclass('{schema}.{table}') as table'''), ).first()
                assert res.table == table

    def test_init_db_idempotent(self):
        runner = CliRunner()
        runner.invoke(init_db)
        runner.invoke(init_db)  # Two call shouln't fail.

@setup_db()
def test_create_new_unkown_nivo_sensor_station():
    with connection_scope() as con:
        res = create_new_unkown_nivo_sensor_station(123456, con)
        assert isinstance(res, RowProxy)
        assert isinstance(res.nss_id, UUID)