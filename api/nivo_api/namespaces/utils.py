from enum import Enum
from uuid import UUID


import shapely.geometry
from flask_restx import fields
from typing import Dict, Union
from geoalchemy2 import WKBElement, WKTElement
from geoalchemy2.shape import to_shape


class UUIDField(fields.Raw):
    __schema_type__ = "string"

    def format(self, value: UUID) -> str:
        return str(value)


class EnumField(fields.Raw):
    __schema_type__ = "string"

    def format(self, value: Enum) -> str:
        return str(value).split(".")[-1]


class GeometryField(fields.Raw):
    def format(self, value: Union[WKTElement, WKBElement]) -> Dict:
        """
        Transform a wkt to geojson
        """
        geom = to_shape(value)
        return shapely.geometry.mapping(geom)
