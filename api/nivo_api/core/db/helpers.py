from typing import List, Union, Dict

from geojson import Feature, FeatureCollection
from sqlalchemy.engine import RowProxy


def _build_feature(db_row: RowProxy, geom_field: str) -> Feature:
    # sanity check
    if not db_row.has_key(geom_field):
        raise KeyError(f"geometry {geom_field} field is not present")
    fields = [f for f in db_row.keys() if f != geom_field]
    geom = db_row[geom_field]
    properties = {}
    for field in fields:
        properties[field] = db_row[field]
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


def to_json(db_row_or_rows: Union[List[RowProxy], RowProxy]) -> Union[List[Dict], Dict]:
    if isinstance(db_row_or_rows, list):
        final_json = list()
        for row in db_row_or_rows:
            final_json.append(to_json(row))
        return final_json
    elif isinstance(db_row_or_rows, RowProxy):
        final_dict = {}
        for k, v in db_row_or_rows.items():
            final_dict[k] = v
        return final_dict
    else:
        raise AssertionError("Rows need to be list of RowProxy or RowProxy.")
