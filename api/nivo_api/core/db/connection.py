from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from flask import current_app, has_app_context
from typing import Optional, Generator

from nivo_api.settings import Config

metadata: MetaData = MetaData()
Base = declarative_base(metadata=metadata)


class DatabaseConnections:
    """
    Hold database connection and scoped session. First use it to put this in flask extension dict.
    """

    orm: Session
    engine: Engine

    def __init__(self):
        self.engine = create_engine(Config.DB_URL)
        self.orm = scoped_session(sessionmaker(bind=self.engine))  # type: ignore
        metadata.bind = self.engine


def create_database_connections() -> "DatabaseConnections":
    return DatabaseConnections()


@contextmanager
def connection_scope(
    engine: Optional[Engine] = None,
) -> Generator[Connection, None, None]:
    """
    Get a SQLAlchemy Engine connection. This method is a context manager. You can either pass the engine to the function
    or, if an app context, get the engine from `current_app` directly (without needing anything).
    """
    if has_app_context() and engine is None:
        engine = current_app.extensions.get("db").engine
    conn = engine.connect()
    try:
        yield conn
    except Exception:
        raise
    finally:
        conn.close()


@contextmanager
def session_scope(session: Optional[Session] = None) -> Generator[Session, None, None]:
    """
    Get a SQLAlchemy session (for ORM). This method is a context manager. You can either pass the session to the function
    or, if an app context, get the engine from `current_app` directly (without needing anything).
    """
    if has_app_context() and session is None:
        session = current_app.extensions.get("db").orm
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.remove()
