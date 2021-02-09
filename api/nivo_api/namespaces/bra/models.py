from flask_restx import fields

from nivo_api.core.api_schema.geojson import (
    Feature as FeatureSchema,
    FeatureCollection as FeatureCollectionSchema,
)
from nivo_api.namespaces.utils import UUIDField, EnumField
from .namespace import bra_api

bra_api.add_model("Feature", FeatureSchema)
bra_api.add_model("FeatureCollection", FeatureCollectionSchema)

zone_model = bra_api.model(
    "ZoneModel",
    {
        "id": UUIDField(attribute="z_id"),
        "name": fields.String(attribute="z_name"),
        "departments": fields.List(
            fields.Nested(
                bra_api.model(
                    "ZoneDepartmentModel",
                    {
                        "id": UUIDField(attribute="d_id"),
                        "name": fields.String(attribute="d_name"),
                        "number": fields.Integer(attribute="d_number"),
                    },
                )
            )
        ),
    },
)

department_model = bra_api.model(
    "DepartmentModel",
    {
        "id": UUIDField(attribute="d_id"),
        "name": fields.String(attribute="d_name"),
        "number": fields.Integer(attribute="d_number"),
        "massifs": fields.List(
            fields.Nested(
                bra_api.model(
                    "DepartmentMassifModel",
                    {
                        "id": UUIDField(attribute="m_id"),
                        "name": fields.String(attribute="m_name"),
                    },
                )
            )
        ),
    },
)

bra_model = bra_api.model(
    "BraModel",
    {
        "id": UUIDField(attribute="br_id"),
        "production_date": fields.DateTime(attribute="br_production_date"),
        "expiration_date": fields.DateTime(attribute="br_expiration_date"),
        "max_risk": fields.Integer(attribute="br_max_risk"),
        "risk_comment": fields.String(attribute="br_risk_comment"),
        "dangerous_slopes": fields.List(EnumField, attribute="br_dangerous_slopes"),
        "dangerous_slopes_comment": fields.String(
            attribute="br_dangerous_slopes_comment"
        ),
        "opinion": fields.String(attribute="br_opinion"),
        "snow_quality": fields.String(attribute="br_snow_quality"),
        "last_snowfall_date": fields.DateTime(attribute="br_last_snowfall_date"),
        "snowlimit_south": fields.Integer(attribute="br_snowlimit_south"),
        "snowlimit_north": fields.Integer(attribute="br_snowlimit_north"),
        "massif": fields.Nested(
            bra_api.model(
                "BraMassifModel",
                {
                    "id": UUIDField(attribute="m_id"),
                    "name": fields.String(attribute="m_name"),
                },
            )
        ),
        "risks": fields.List(
            fields.Nested(
                bra_api.model(
                    "BraRisksModel",
                    {
                        "id": UUIDField(attribute="r_id"),
                        "altitude_limit": fields.String(attribute="r_altitude_limit"),
                        "risk": fields.Integer(attribute="r_risk"),
                        "evolution": fields.Integer(attribute="r_evolution"),
                    },
                )
            )
        ),
        "snow_records": fields.List(
            fields.Nested(
                bra_api.model(
                    "SnowRecordsModel",
                    {
                        "id": UUIDField(attribute="s_id"),
                        "altitude": fields.Integer(attribute="s_altitude"),
                        "snow_quantity_cm_north": fields.Integer(
                            attribute="s_snow_quantity_cm_north"
                        ),
                        "snow_quantity_cm_south": fields.Integer(
                            attribute="s_snow_quantity_cm_south"
                        ),
                    },
                )
            )
        ),
        "fresh_snow_records": fields.List(
            fields.Nested(
                bra_api.model(
                    "FreshSnowRecordModel",
                    {
                        "id": UUIDField(attribute="fsr_id"),
                        "date": fields.DateTime(attribute="fsr_date"),
                        "altitude": fields.Integer(attribute="fsr_altitude")
                        # TODO add submassif
                    },
                )
            )
        ),
        "weather_forecasts": fields.List(
            fields.Nested(
                bra_api.model(
                    "WeatherForecastsRecordModel",
                    {
                        "id": UUIDField(attribute="wf_id"),
                        "expected_date": fields.DateTime(attribute="wf_expected_date"),
                        "weather_type": EnumField(attribute="wf_weather_type"),
                        "sea_of_clouds": fields.Integer(attribute="wf_sea_of_clouds"),
                        "rain_snow_limit": fields.Integer(
                            attribute="wf_rain_snow_limit"
                        ),
                        "iso0": fields.Integer(attribute="wf_iso0"),
                        "iso_minus_10": fields.Integer(attribute="wf_iso_minus_10"),
                    },
                )
            )
        ),
        "risk_forecasts": fields.List(
            fields.Nested(
                bra_api.model(
                    "RiskForecastsRecordModel",
                    {
                        "id": UUIDField(attribute="rf_id"),
                        "date": fields.Date(attribute="rf_date"),
                        "evolution": EnumField(attribute="rf_evolution"),
                    },
                )
            )
        ),
    },
)


massifs_model = bra_api.model(
    "MassifsModel",
    {
        "id": UUIDField(attribute="m_id"),
        "name": fields.String(attribute="m_name"),
        "department": {
                    "id": UUIDField(attribute="d_id"),
                    "name": fields.String(attribute="d_name"),
                    "number": fields.Integer(attribute="d_number"),
                },
        "latest_record": {
            "id": UUIDField(attribute="br_id"),
            "max_risk": fields.Integer(attribute="br_max_risk"),
            "date": fields.DateTime(attribute="br_production_date"),
            "dangerous_slopes": fields.List(EnumField, attribute="br_dangerous_slopes"),
            "snowlimit_south": fields.Integer(attribute="br_snowlimit_south"),
            "snowlimit_north": fields.Integer(attribute="br_snowlimit_north"),
            "risks": fields.List(
                fields.Nested(
                    bra_api.model(
                        "MassifsLastestRecordRisks",
                        {
                            "id": UUIDField(attribute="r_id"),
                            "risk": fields.Integer(attribute="r_risk"),
                            "altitude": fields.String(attribute="r_altitude_limit"),
                        },
                    )
                )
            ),
        },
    },
)
