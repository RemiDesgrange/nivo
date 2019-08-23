import logging

from nivo_api.core.db.connection import db_engine
from nivo_api.core.db.models.sql.bra import *


def create_schema_and_table(drop: bool) -> None:
    if drop:
        metadata.drop_all(db_engine)
        db_engine.execute("DROP SCHEMA IF EXISTS nivo CASCADE")
        db_engine.execute("DROP SCHEMA IF EXISTS bra CASCADE")

    db_engine.execute("CREATE SCHEMA IF NOT EXISTS nivo")
    db_engine.execute("CREATE SCHEMA IF NOT EXISTS bra")
    metadata.create_all(db_engine)
