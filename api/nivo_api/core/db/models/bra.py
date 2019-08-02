import uuid
from enum import Enum

from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    TEXT,
    Integer,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Boolean,
    Date,
)

from nivo_api.core.db.connection import metadata
from nivo_api.core.db.models import AbstractSpatialTable, AbstractTable
from sqlalchemy.dialects.postgresql import UUID, ENUM

# XML data model : https://donneespubliques.meteofrance.fr/client/document/docbraxml_248.pdf

# french department. The polygon is extract from OSM.
from nivo_api.core.db.models.helper import ArrayOfEnum, XML

Department = AbstractSpatialTable(
    "bra_department",
    metadata,
    Column("bd_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("bd_name", TEXT, unique=True, nullable=False),
    Column("bd_number", Integer, unique=True),
    Column("bd_zone", UUID(as_uuid=True), ForeignKey("bra_zone.bz_id"), nullable=False),
    Column("the_geom", Geometry("MULTIPOLYGON", srid=4326), nullable=False),
)
# "North Alps", "Souith Alps" etc...
Zone = AbstractSpatialTable(
    "bra_zone",
    metadata,
    Column("bz_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("bz_name", TEXT, unique=True, nullable=False),
)
# Alpine massif, like "Maurienne", "Chablais", "Aspe ossau"
Massif = AbstractSpatialTable(
    "bra_massif",
    metadata,
    Column("bm_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("bm_name", TEXT, unique=True, nullable=False),
    Column(
        "bm_department",
        UUID(as_uuid=True),
        ForeignKey("bra_department.bd_id"),
        nullable=False,
    ),
    Column("the_geom", Geometry("POLYGON", srid=4326), nullable=False),
)

Risk = AbstractTable(
    "bra_risk",
    metadata,
    Column("r_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "r_number",
        Integer,
        CheckConstraint("r_number>0 AND r_number<5"),
        unique=True,
        nullable=False,
    ),
    Column("r_description", TEXT),
)


class DangerousSlopes(Enum):
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"
    N = "N"


# actual implemntation in the DB
_PGDangerousSlopes = ENUM(DangerousSlopes, name="dangerous_slopes_t", metadata=metadata)

BraRecord = AbstractTable(
    "bra_record",
    metadata,
    Column("br_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "br_massif", UUID(as_uuid=True), ForeignKey("bra_massif.bm_id"), nullable=False
    ),
    Column("br_production_date", DateTime, nullable=False),
    Column("br_expiration_date", DateTime, nullable=False),
    Column("br_is_amended", Boolean),
    Column("br_max_risk", ForeignKey("bra_risk.r_id")),
    Column("br_risk1", ForeignKey("bra_risk.r_id")),
    Column("br_risk1_altitude_limit", TEXT),
    Column("br_risk1_evolution", ForeignKey("bra_risk.r_id")),
    Column("br_risk2", ForeignKey("bra_risk.r_id")),
    Column("br_risk2_altitude_limit", TEXT),
    Column("br_risk2_evolution", ForeignKey("bra_risk.r_id")),
    Column("br_risk_comment", TEXT),
    Column("br_dangerous_slopes", ArrayOfEnum(_PGDangerousSlopes)),
    Column("br_dangerous_slopes_comment", TEXT),
    Column("br_opinion", TEXT),
    Column("br_snow_quality", TEXT),
    Column("br_snow_stability", TEXT),
    Column("br_last_snowfall_date", Date),
    Column("br_snowlimit_south", Integer, CheckConstraint("br_snowlimit_south>0")),
    Column("br_snowlimit_north", Integer, CheckConstraint("br_snowlimit_north>0")),
    Column("br_raw_xml", XML, nullable=False),
)

BraSnowRecord = AbstractTable(
    "bra_snow_record",
    metadata,
    Column("s_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "s_bra_record",
        UUID(as_uuid=True),
        ForeignKey("bra_record.br_id"),
        nullable=False,
    ),
    Column("s_altitude", Integer, CheckConstraint("s_altitude>0"), nullable=False),
    Column(
        "s_snow_quantity_cm_north",
        Integer,
        CheckConstraint("s_snow_quantity_cm_north>0"),
        nullable=False,
    ),
    Column(
        "s_snow_quantity_cm_south",
        Integer,
        CheckConstraint("s_snow_quantity_cm_south>0"),
        nullable=False,
    ),
)
BraFreshSnowRecord = AbstractTable(
    "bra_fresh_snow_record",
    metadata,
    Column("bfsr_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "bfsr_bra_record",
        UUID(as_uuid=True),
        ForeignKey("bra_record.br_id"),
        nullable=False,
    ),
    Column("bfsr_date", DateTime, nullable=False),
    Column("bfsr_altitude", Integer, CheckConstraint("bfsr_altitude>0")),
    Column("bsfr_massif_snowfall", Integer, nullable=False),
    # in meteofrance data, if no submassif, then this value takes "-1". This is bullshit.
    # we use NULL as a "non existance of value" here.
    Column("bfsr_second_massif_snowfall", Integer),
)
WeatherForcast = AbstractTable(
    "bra_weather_forcast",
    metadata,
    Column("wf_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "wf_bra_record",
        UUID(as_uuid=True),
        ForeignKey("bra_record.br_id"),
        nullable=False,
    ),
    Column("wf_expected_date", DateTime, nullable=False),
    Column(
        "wf_wind_altitude",
        Integer,
        CheckConstraint("wf_wind_altitude>0"),
        nullable=False,
    ),
    # Maybe an ENUM or a table
    Column("wf_weather_type", Integer, nullable=False),
    Column("wf_sea_of_clouds", Integer),
    Column("wf_rain_snow_limit", Integer, CheckConstraint("wf_rain_snow_limit>0")),
    Column("wf_iso0", Integer, CheckConstraint("wf_iso0>0")),
    Column("wf_iso_minus_10", Integer, CheckConstraint("wf_iso_minus_10>0")),
    Column("wf_wind_direction", TEXT, nullable=False),
    Column(
        "wf_wind_force", Integer, CheckConstraint("wf_wind_force>0"), nullable=False
    ),
)

RiskEvolution = ENUM("UP", "DOWN", "STABLE", name="risk_evolution_t", metadata=metadata)

RiskForcast = AbstractTable(
    "bra_risk_forcast",
    metadata,
    Column("rf_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("rf_bra_record", UUID(as_uuid=True), ForeignKey("bra_record.br_id")),
    Column("rf_date", Date, nullable=False),
    Column("rf_evolution", RiskEvolution),
)
