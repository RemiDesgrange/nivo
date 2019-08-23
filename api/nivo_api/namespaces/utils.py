from uuid import UUID


import shapely.geometry
from flask_restplus import fields
from typing import Dict, Union
from geoalchemy2 import WKBElement, WKTElement
from geoalchemy2.shape import to_shape


class UUIDField(fields.Raw):
    def format(self, value: UUID) -> str:
        return str(value)


class GeometryField(fields.Raw):
    def format(self, value: Union[WKTElement, WKBElement]) -> Dict:
        """
        Transform a wkt to geojson
        """
        geom = to_shape(value)
        return shapely.geometry.mapping(geom)
