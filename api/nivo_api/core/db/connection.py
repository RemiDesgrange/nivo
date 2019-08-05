from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine, Connection

from nivo_api.settings import Config


# Global Instance of metadata
metadata: MetaData = MetaData()
db_engine: Engine = create_engine(Config.DB_URL)


@contextmanager
def connection_scope(engine: Engine = None) -> Connection:
    engine = engine or db_engine
    conn = engine.connect()
    try:
        yield conn
    except:
        raise
    finally:
        conn.close()
