from sqlalchemy.orm import relationship

from nivo_api.core.db.connection import Base
from nivo_api.core.db.models.sql.bra import (
    DepartmentTable,
    ZoneTable,
    MassifTable,
    RiskTable,
    BraRecordTable,
    SnowRecordTable,
    FreshSnowRecordTable,
    WeatherForcastTable,
    WeatherForcastAtAltitudeTable,
    RiskForcastTable,
)


class Department(Base):
    __table__ = DepartmentTable
    massifs = relationship("Massif", back_populates="department")
    zone = relationship("Zone", back_populates="departments")


class Zone(Base):
    __table__ = ZoneTable
    departments = relationship("Department", back_populates="zone")


class Massif(Base):
    __table__ = MassifTable
    department = relationship("Department", back_populates="massifs")


class Risk(Base):
    __table__ = RiskTable
    bra_record = relationship("BraRecord", back_populates="risks")


class BraRecord(Base):
    __table__ = BraRecordTable
    risks = relationship("Risk", back_populates="bra_record")
    snow_records = relationship("SnowRecord", back_populates="bra_record")
    fresh_snow_records = relationship("FreshSnowRecord", back_populates="bra_record")
    weather_forcasts = relationship("WeatherForcast", back_populates="bra_record")
    risk_forcasts = relationship("RiskForcast", back_populates="bra_record")
    massif = relationship("Massif")


class SnowRecord(Base):
    __table__ = SnowRecordTable
    bra_record = relationship("BraRecord", back_populates="snow_records")


class FreshSnowRecord(Base):
    __table__ = FreshSnowRecordTable
    bra_record = relationship("BraRecord", back_populates="fresh_snow_records")


class WeatherForcast(Base):
    __table__ = WeatherForcastTable
    bra_record = relationship("BraRecord", back_populates="weather_forcasts")
    weather_forcasts_at_altitude = relationship(
        "WeatherForcastAtAltitude", back_populates="weather_forcast"
    )


class WeatherForcastAtAltitude(Base):
    __table__ = WeatherForcastAtAltitudeTable
    weather_forcast = relationship(
        "WeatherForcast", back_populates="weather_forcasts_at_altitude"
    )


class RiskForcast(Base):
    __table__ = RiskForcastTable
    bra_record = relationship("BraRecord", back_populates="risk_forcasts")
