from sqlalchemy.orm import relationship

from nivo_api.core.db.connection import Base
from nivo_api.core.db.models.sql.nivo import NivoRecordTable, SensorStationTable


class SensorStation(Base):
    __table__ = SensorStationTable
    records = relationship("NivoRecord", back_populates="sensor_station")


class NivoRecord(Base):
    __table__ = NivoRecordTable
    sensor_station = relationship("SensorStation", back_populates="records")
