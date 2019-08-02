"""
Create custom flask restplus schemamodel to return
"""
import json
import os
from pathlib import Path

from flask_restplus import SchemaModel


_current_path = Path(os.path.dirname(os.path.realpath(__file__)))
_feature_json = os.path.join(_current_path, "../json_schema/Feature.json")
_featurecollection_json = os.path.join(
    _current_path, "../json_schema/FeatureCollection.json"
)


Feature = SchemaModel("Feature", json.load(open(_feature_json)))
FeatureCollection = SchemaModel(
    "FeatureCollection", json.load(open(_featurecollection_json))
)
