from nivo_api.core.db.connection import metadata, create_database_connections
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ProgrammingError


def is_postgis_installed(engine: Engine) -> bool:
    try:
        engine.execute("SELECT postgis_version()")
        return True
    except ProgrammingError:
        return False


def create_schema_and_table(drop: bool) -> None:
    schema = ["bra", "nivo", "flowcapt"]
    db_con = create_database_connections()
    if not is_postgis_installed(db_con.engine):
        db_con.engine.execute("CREATE EXTENSION postgis")

    if drop:
        metadata.drop_all(db_con.engine)
        [db_con.engine.execute(f"DROP SCHEMA IF EXISTS {s} CASCADE") for s in schema]

    [db_con.engine.execute(f"CREATE SCHEMA IF NOT EXISTS {s}") for s in schema]
    metadata.create_all(db_con.engine)
