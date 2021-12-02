from sqlalchemy.orm import relationship
from sqlalchemy import func, text
from sqlalchemy.orm import column_property

from nivo_api.core.db.connection import Base
from nivo_api.core.db.models.sql.bra import (
    DepartmentTable,
    ZoneTable,
    MassifTable,
    RiskTable,
    BraRecordTable,
    SnowRecordTable,
    FreshSnowRecordTable,
    WeatherForecastTable,
    WeatherForecastAtAltitudeTable,
    RiskForecastTable,
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
    weather_forecasts = relationship("WeatherForecast", back_populates="bra_record")
    risk_forecasts = relationship("RiskForecast", back_populates="bra_record")
    massif = relationship("Massif")
    previous_bra_id = column_property(
        func.lag(text("br_id")).over(
            order_by=text("br_production_date"), partition_by=text("br_massif")
        ).label("previous_bra_id")
    )
    next_bra_id = column_property(
        func.lead(text("br_id")).over(
            order_by=text("br_production_date"), partition_by=text("br_massif")
        ).label("next_bra_id")
    )


class SnowRecord(Base):
    __table__ = SnowRecordTable
    bra_record = relationship("BraRecord", back_populates="snow_records")


class FreshSnowRecord(Base):
    __table__ = FreshSnowRecordTable
    bra_record = relationship("BraRecord", back_populates="fresh_snow_records")


class WeatherForecast(Base):
    __table__ = WeatherForecastTable
    bra_record = relationship("BraRecord", back_populates="weather_forecasts")
    weather_forecasts_at_altitude = relationship(
        "WeatherForecastAtAltitude", back_populates="weather_forecast"
    )


class WeatherForecastAtAltitude(Base):
    __table__ = WeatherForecastAtAltitudeTable
    weather_forecast = relationship(
        "WeatherForecast", back_populates="weather_forecasts_at_altitude"
    )


class RiskForecast(Base):
    __table__ = RiskForecastTable
    bra_record = relationship("BraRecord", back_populates="risk_forecasts")
