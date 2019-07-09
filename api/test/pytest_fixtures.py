from contextlib import contextmanager

from nivo_api.core.db.connection import metadata, db_engine


@contextmanager
def setup_db():
    metadata.drop_all(db_engine)
    metadata.create_all(db_engine)
    yield
    metadata.drop_all(db_engine)