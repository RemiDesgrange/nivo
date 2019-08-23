import uuid
from enum import Enum, IntEnum

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

from nivo_api.core.db.models.sql.helper import ArrayOfEnum, XML


# XML data model : https://donneespubliques.meteofrance.fr/client/document/docbraxml_248.pdf

# Abstract Enum. To represent direction. see below.
class Direction(Enum):
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"
    N = "N"
    ALL = "_"


# impl for dangerous slopes direction. Cannot subclass Enum
DangerousSlopes = Direction

# impl for wind direction. Cannot subclass Enum
WindDirection = Direction


class WeatherType(IntEnum):
    SUN_OR_CLEAR_NIGHT = 1
    OVERCAST_SUN_OR_OVERCAST_SKY = 2
    SUN_OR_CLOUDY = 3
    THINNING_SKY = 4
    VERY_CLOUDY_SHORT_THINNING = 5
    CLOUDY = 6
    SUN_WITH_RAIN = 7
    CLOUDY_WITH_RAIN = 8
    CLOUDY_WITH_MODERATE_TO_HEAVY_RAIN = 9
    CLOUDY_WITH_SNOWFALL = 10
    SUN_WITH_SOME_SNOWFALL = 11
    MODERATE_TO_HEAVY_SNOWFALL = 12
    ISOLATED_THUNDER = 13
    THUNDER = 14
    FOG = 15
    FREEZING_FOG = 16
    FREEZING = 17
    SEA_OF_CLOUDS = 18


class RiskEvolution(IntEnum):
    STABLE = 0
    UP = 0
    DOWN = -1
    UNKNOWN = -2


# french department. The polygon is extracted from OSM.
DepartmentTable = AbstractSpatialTable(
    "department",
    metadata,
    Column("d_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("d_name", TEXT, unique=True, nullable=False),
    Column("d_number", Integer, unique=True),
    Column("d_zone", UUID(as_uuid=True), ForeignKey("bra.zone.z_id"), nullable=False),
    schema="bra",
)
# "North Alps", "Souith Alps" etc...
ZoneTable = AbstractSpatialTable(
    "zone",
    metadata,
    Column("z_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("z_name", TEXT, unique=True, nullable=False),
    schema="bra",
)
# Alpine massif, like "Maurienne", "Chablais", "Aspe ossau"
MassifTable = AbstractSpatialTable(
    "massif",
    metadata,
    Column("m_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("m_name", TEXT, unique=True, nullable=False),
    Column(
        "m_department",
        UUID(as_uuid=True),
        ForeignKey("bra.department.d_id"),
        nullable=False,
    ),
    Column("the_geom", Geometry("POLYGON", srid=4326), nullable=False),
    schema="bra",
)

RiskTable = AbstractTable(
    "risk",
    metadata,
    Column("r_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "r_record_id",
        UUID(as_uuid=True),
        ForeignKey("bra.record.br_id"),
        nullable=False,
    ),
    Column("r_altitude_limit", TEXT),
    Column("r_risk", Integer, CheckConstraint("r_risk>0 AND r_risk<5")),
    Column("r_evolution", Integer, CheckConstraint("r_evolution>0 AND r_evolution<5")),
    schema="bra",
)

# actual implemntation in the DB
_PGDangerousSlopes = ENUM(DangerousSlopes, name="dangerous_slopes_t", metadata=metadata, schema="bra")

BraRecordTable = AbstractTable(
    "record",
    metadata,
    Column("br_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "br_massif", UUID(as_uuid=True), ForeignKey("bra.massif.m_id"), nullable=False
    ),
    Column("br_production_date", DateTime, nullable=False),
    Column("br_expiration_date", DateTime, nullable=False),
    Column("br_is_amended", Boolean),
    Column(
        "br_max_risk",
        Integer,
        CheckConstraint("br_max_risk>0 AND br_max_risk<=5"),
        nullable=False,
    ),
    Column("br_risk_comment", TEXT),
    Column("br_dangerous_slopes", ArrayOfEnum(_PGDangerousSlopes)),
    Column("br_dangerous_slopes_comment", TEXT),
    Column("br_opinion", TEXT),
    Column("br_snow_quality", TEXT),
    Column("br_snow_stability", TEXT),
    Column("br_last_snowfall_date", Date),
    Column("br_snowlimit_south", Integer, CheckConstraint("br_snowlimit_south>=-1")),
    Column("br_snowlimit_north", Integer, CheckConstraint("br_snowlimit_north>=-1")),
    Column("br_raw_xml", XML, nullable=False),
    schema="bra",
)

SnowRecordTable = AbstractTable(
    "snow_record",
    metadata,
    Column("s_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "s_bra_record",
        UUID(as_uuid=True),
        ForeignKey("bra.record.br_id"),
        nullable=False,
    ),
    Column("s_altitude", Integer, CheckConstraint("s_altitude>0"), nullable=False),
    Column(
        "s_snow_quantity_cm_north",
        Integer,
        CheckConstraint("s_snow_quantity_cm_north>=0"),
        nullable=False,
    ),
    Column(
        "s_snow_quantity_cm_south",
        Integer,
        CheckConstraint("s_snow_quantity_cm_south>=0"),
        nullable=False,
    ),
    schema="bra",
)
FreshSnowRecordTable = AbstractTable(
    "fresh_snow_record",
    metadata,
    Column("fsr_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "fsr_bra_record",
        UUID(as_uuid=True),
        ForeignKey("bra.record.br_id"),
        nullable=False,
    ),
    Column("fsr_date", DateTime, nullable=False),
    Column("fsr_altitude", Integer, CheckConstraint("fsr_altitude>0")),
    Column("sfr_massif_snowfall", Integer, nullable=False),
    # in meteofrance data, if no submassif, then this value takes "-1". This is bullshit.
    # we use NULL as a "non existance of value" here.
    Column("fsr_second_massif_snowfall", Integer),
    schema="bra",
)

_PGWeatherType = ENUM(WeatherType, name="weather_type_t", metadata=metadata, schema="bra")

WeatherForcastTable = AbstractTable(
    "weather_forcast",
    metadata,
    Column("wf_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "wf_bra_record",
        UUID(as_uuid=True),
        ForeignKey("bra.record.br_id"),
        nullable=False,
    ),
    Column("wf_expected_date", DateTime, nullable=False),
    # Maybe an ENUM or a table
    Column("wf_weather_type", _PGWeatherType, nullable=False),
    Column("wf_sea_of_clouds", Integer, nullable=False),
    Column(
        "wf_rain_snow_limit",
        Integer,
        CheckConstraint("wf_rain_snow_limit>=0 OR wf_rain_snow_limit=-1"),
        nullable=False,
    ),
    Column("wf_iso0", Integer, CheckConstraint("wf_iso0>0"), nullable=False),
    Column(
        "wf_iso_minus_10", Integer, CheckConstraint("wf_iso_minus_10>0"), nullable=False
    ),
    schema="bra",
)

_PGWindDirection = ENUM(
    WindDirection, name="wind_direction_t", metadata=metadata, schema="bra"
)

WeatherForcastAtAltitudeTable = AbstractTable(
    "weather_forcast_at_altitude",
    metadata,
    Column("wfaa_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "wfaa_wf_id",
        UUID(as_uuid=True),
        ForeignKey("bra.weather_forcast.wf_id"),
        nullable=False,
    ),
    Column(
        "wfaa_wind_altitude",
        Integer,
        CheckConstraint("wfaa_wind_altitude>0"),
        nullable=False,
    ),
    # this should be a enum, maybe.
    Column("wfaa_wind_direction", _PGWindDirection, nullable=False),
    Column(
        "wfaa_wind_force",
        Integer,
        CheckConstraint("wfaa_wind_force>=0"),
        nullable=False,
    ),
    schema="bra",
)

_PGRiskEvolution = ENUM(
    RiskEvolution, name="risk_evolution_t", metadata=metadata, schema="bra"
)

RiskForcastTable = AbstractTable(
    "risk_forcast",
    metadata,
    Column("rf_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("rf_bra_record", UUID(as_uuid=True), ForeignKey("bra.record.br_id")),
    Column("rf_date", Date, nullable=False),
    Column("rf_evolution", _PGRiskEvolution),
    schema="bra",
)
