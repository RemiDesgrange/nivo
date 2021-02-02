from geojson import Feature
from sqlalchemy import select

from nivo_api.cli import persist_flowcapt_station
from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.sql.flowcapt import FlowCaptStationTable

from test.pytest_fixtures import database


def test_expected_json(database):
    test_f = Feature(
        properties={
            "id": "FBER1",
            "site": "La Berarde",
            "altitude": 2390,
            "country": "France",
        },
        geometry={"type": "Point", "coordinates": [6.237082, 44.949944]},
    )
    with connection_scope(database.engine) as con:
        persist_flowcapt_station(con, test_f)
        res = con.execute(select([FlowCaptStationTable])).fetchall()
        assert len(res) == 1
        assert res[0].fcs_id == "FBER1"
