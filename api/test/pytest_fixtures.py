from contextlib import contextmanager


from nivo_api.core.db.connection import metadata, db_engine


schema = ["bra", "nivo", "flowcapt"]


@contextmanager
def setup_db():
    [db_engine.execute(f"DROP SCHEMA IF EXISTS {s} CASCADE") for s in schema]
    [db_engine.execute(f"CREATE SCHEMA IF NOT EXISTS {s}") for s in schema]
    metadata.create_all(db_engine)
    yield
    [db_engine.execute(f"DROP SCHEMA IF EXISTS {s} CASCADE") for s in schema]
