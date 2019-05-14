from typing import List, Union, Dict

from sqlalchemy.engine import RowProxy


def _check_geom(geom: Dict) -> Dict:
    assert isinstance(geom, dict), f"geom of type {type(geom)}"
    # see https://tools.ietf.org/html/rfc7946#section-1.4
    assert 'type' in geom
    assert 'coordinates' in geom
    assert geom['type'].upper() in ['POINT',
                                    'MULTIPOINT',
                                    'LINESTRING',
                                    'MULTILINESTRING',
                                    'POLYGON',
                                    'MULTIPOLYGON',
                                    'GEOMETRYCOLLECTION']
    assert isinstance(geom['coordinates'], (dict, list))
    return geom


def _build_feature(db_row: RowProxy, geom_field: str) -> Dict:
    final_dict = {
        "type": "Feature",
        "geometry": None,
        "properties": {}
    }
    for field, value in db_row.items():
        if field == geom_field:
            final_dict['geometry'] = _check_geom(value)
        else:
            final_dict["properties"][field] = value
    return final_dict


def _build_featurecollection(db_rows: List[RowProxy], geom_field: str) -> Dict:
    return {
        'type': 'FeatureCollection',
        'features': [
            _build_feature(feat, geom_field) for feat in db_rows
        ]
    }


def to_geojson(db_row_or_rows: Union[List[RowProxy], RowProxy], geom_field: str = 'the_geom') -> Dict:
    if isinstance(db_row_or_rows, List):
        return _build_featurecollection(db_row_or_rows, geom_field)
    elif isinstance(db_row_or_rows, RowProxy):
        return _build_feature(db_row_or_rows, geom_field)
