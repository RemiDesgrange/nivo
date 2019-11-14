import click

from nivo_api.core.db.models.sql.flowcapt import *
from nivo_api.core.db.models.sql.nivo import *
from nivo_api.core.db.models.sql.bra import *

from nivo_api.core.db.connection import metadata, db_engine

def create_schema_and_table(drop: bool) -> None:
    schema = ['bra', "nivo", "flowcapt"]
    click.echo(metadata.sorted_tables)
    if drop:
        metadata.drop_all(db_engine)
        [db_engine.execute(f"DROP SCHEMA IF EXISTS {s} CASCADE") for s in schema]

    [db_engine.execute(f"CREATE SCHEMA IF NOT EXISTS {s}") for s in schema]
    metadata.create_all(db_engine)
