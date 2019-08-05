from typing import List, Union

from geojson import Feature, FeatureCollection
from sqlalchemy.engine import RowProxy


def _build_feature(db_row: RowProxy, geom_field: str) -> Feature:
    # sanity check
    if not db_row.has_key(geom_field):
        raise KeyError(f"geometry {geom_field} field is not present")
    geom = db_row.pop(geom_field)
    properties = {}
    for field, value in db_row.items():
        properties[field] = value
    feature = Feature(geometry=geom, properties=properties)
    return feature


def _build_featurecollection(
    db_rows: List[RowProxy], geom_field: str
) -> FeatureCollection:
    return FeatureCollection([_build_feature(feat, geom_field) for feat in db_rows])


def to_geojson(
    db_row_or_rows: Union[List[RowProxy], RowProxy], geom_field: str = "the_geom"
) -> Union[Feature, FeatureCollection]:
    if isinstance(db_row_or_rows, List):
        return _build_featurecollection(db_row_or_rows, geom_field)
    elif isinstance(db_row_or_rows, RowProxy):
        return _build_feature(db_row_or_rows, geom_field)
