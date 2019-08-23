import uuid

from geoalchemy2 import Geometry
from sqlalchemy import Column, TEXT, Integer, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from nivo_api.core.db.connection import metadata

from nivo_api.core.db.models import AbstractSpatialTable, AbstractTable

# position of all the sensor. Usually in ski resort.
SensorStationTable = AbstractSpatialTable(
    "sensor_stations",
    metadata,
    Column("nss_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("nss_name", TEXT, unique=True, nullable=False),
    Column("nss_meteofrance_id", Integer, unique=True),
    Column("the_geom", Geometry("POINTZ", srid=4326, dimension=3), nullable=False),
    schema="nivo",
)

# Snow data from a sensor station.
NivoRecordTable = AbstractTable(
    "records",
    metadata,
    Column("nr_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("nr_date", DateTime, nullable=False),
    Column("nr_haut_sta", Float),
    Column("nr_dd", Integer),
    Column("nr_ff", Float),
    Column("nr_t", Float),
    Column("nr_td", Float),
    Column("nr_u", Integer),
    Column("nr_ww", Integer),
    Column("nr_w1", Integer),
    Column("nr_w2", Integer),
    Column("nr_n", Float),
    Column("nr_nbas", Integer),
    Column("nr_hbas", Integer),
    Column("nr_cl", Integer),
    Column("nr_cm", Integer),
    Column("nr_ch", Integer),
    Column("nr_rr24", Float),
    Column("nr_tn12", Float),
    Column("nr_tn24", Float),
    Column("nr_tx12", Float),
    Column("nr_tx24", Float),
    Column("nr_ht_neige", Float),
    Column("nr_ssfrai", Float),
    Column("nr_perssfrai", Float),
    Column("nr_phenspe1", Float),
    Column("nr_phenspe2", Float),
    Column("nr_nnuage1", Integer),
    Column("nr_t_neige", Float),
    Column("nr_etat_neige", Integer),
    Column("nr_prof_sonde", Integer),
    Column("nr_nuage_val", Integer),
    Column("nr_chasse_neige", Integer),
    Column("nr_aval_descr", Integer),
    Column("nr_aval_genre", Integer),
    Column("nr_aval_depart", Integer),
    Column("nr_aval_expo", Integer),
    Column("nr_aval_risque", Integer),
    Column("nr_dd_alti", Integer),
    Column("nr_ff_alti", Float),
    Column("nr_ht_neige_alti", Float),
    Column("nr_neige_fraiche", Float),
    Column("nr_teneur_eau", Integer),
    Column("nr_grain_predom", Integer),
    Column("nr_grain_nombre", Integer),
    Column("nr_grain_diametr", Integer),
    Column("nr_homogeneite", Integer),
    Column("nr_m_vol_neige", Float),
    Column(
        "nr_nivo_sensor",
        UUID(as_uuid=True),
        ForeignKey("nivo.sensor_stations.nss_id"),
        nullable=False,
    ),
    schema="nivo",
)

# Since all the field are not quite obvious. Document the field
NivoRecordDescriptionTable = AbstractTable(
    "record_descriptions",
    metadata,
    Column("nrd_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("nrd_name", TEXT, nullable=False),
    Column("nrd_description", TEXT, nullable=False),
    Column("nrd_unit", TEXT, nullable=True),
    Column("nrd_type", TEXT, nullable=True),
    schema="nivo",
)
