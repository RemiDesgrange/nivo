from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from nivo_api.settings import Config


# Global Instance of metadata
metadata: MetaData = MetaData()
db_engine: Engine = create_engine(Config.DB_URL)
Base = declarative_base(metadata=metadata)
DBSession = scoped_session(sessionmaker(bind=db_engine))


@contextmanager
def connection_scope(engine: Engine = None) -> Connection:
    engine = engine or db_engine
    conn = engine.connect()
    try:
        yield conn
    except Exception:
        raise
    finally:
        conn.close()


@contextmanager
def session_scope():
    sess: Session = DBSession()
    try:
        yield sess
    except:
        sess.rollback()
        raise
    finally:
        DBSession.remove()