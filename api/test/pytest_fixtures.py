from contextlib import contextmanager

from sqlalchemy import create_engine

from nivo_api.core.db.connection import metadata, db_engine


schema = ["bra", "nivo", "flowcapt"]


@contextmanager
def setup_db():
    test_engine = create_engine("postgresql://nivo:nivo@localhost:5432/nivo_test")
    global db_engine
    [test_engine.execute(f"DROP SCHEMA IF EXISTS {s} CASCADE") for s in schema]
    [test_engine.execute(f"CREATE SCHEMA IF NOT EXISTS {s}") for s in schema]
    metadata.bind = test_engine
    metadata.create_all(test_engine)
    original_engine = db_engine
    db_engine = test_engine
    yield
    db_engine = original_engine
    [test_engine.execute(f"DROP SCHEMA IF EXISTS {s} CASCADE") for s in schema]
