from contextlib import contextmanager
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from nivo_api.settings import Config


def _get_engine(engine: Optional[Engine]) -> Engine:
    assert isinstance(engine, Engine) or engine is None, 'engine should be None or Engine instance'
    if isinstance(engine, Engine):
        return engine
    else:
        return create_engine(Config.DB_URL)



@contextmanager
def connection_scope(engine: Engine=None):
    engine = _get_engine(engine)
    try:
        conn = engine.connect()
        yield conn
    except Exception as e:
        raise e
    finally:
        conn.close()