import pytest

from nivo_api.core.db.connection import create_database_connections, metadata

schema = ["bra", "nivo", "flowcapt"]


@pytest.fixture
def database():
    db_con = create_database_connections()
    [db_con.engine.execute(f"DROP SCHEMA IF EXISTS {s} CASCADE") for s in schema]
    [db_con.engine.execute(f"CREATE SCHEMA IF NOT EXISTS {s}") for s in schema]
    metadata.create_all(db_con.engine)
    yield db_con
    [db_con.engine.execute(f"DROP SCHEMA IF EXISTS {s} CASCADE") for s in schema]
