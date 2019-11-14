

from geoalchemy2 import Geometry
from sqlalchemy import TEXT, Column, Integer

from nivo_api.core.db.connection import metadata
from nivo_api.core.db.models import AbstractSpatialTable

FlowCaptStationTable = AbstractSpatialTable(
    "flowcapt_stations",
    metadata,
    Column("fcs_id", TEXT, primary_key=True),
    Column("fcs_site", TEXT, nullable=False),
    Column("fcs_country", TEXT, nullable=False),
    Column("fcs_altitude", Integer, nullable=False),
    Column("the_geom", Geometry("POINT", srid=4326), nullable=False),
    schema="flowcapt",
)