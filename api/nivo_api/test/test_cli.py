from click.testing import CliRunner
from sqlalchemy import text

from nivo_api.cli import init_db
from nivo_api.core.db.connection import metadata, db_engine, connection_scope
from nivo_api.core.db.models.nivo import *


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
