from nivo_api.core.db.connection import metadata, db_engine
from nivo_api.core.db.models.nivo import *


def create_schema_and_table():
    metadata.create_all(db_engine)