from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape
from geojson import Feature
from shapely.geometry import shape
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from nivo_api.core.db.models.sql.flowcapt import FlowCaptStationTable


def persist_flowcapt_station(con: Connection, station: Feature) -> None:
    geom = _get_geom(station)
    ins = insert(FlowCaptStationTable).values(
        fcs_id=station.properties["id"],
        fcs_site=station.properties["site"],
        fcs_country=station.properties["country"],
        fcs_altitude=station.properties["altitude"],
        the_geom=geom,
    )
    ins = ins.on_conflict_do_nothing(index_elements=["fcs_id"])
    con.execute(ins)


def _get_geom(station: Feature) -> WKBElement:
    return from_shape(shape(station.geometry), 4326)
