import pytest


from nivo_api.core.db.helpers import _build_feature, _build_featurecollection
from test.helpers_for_tests import FakeRowProxy


class TestBuildFeature:
    def test_wrong_geom(self):

        geodata_exemple = FakeRowProxy(
            {"geom": None, "test1": "test1", "pom": 1}.items()
        )
        with pytest.raises(KeyError) as e:
            _build_feature(geodata_exemple, "blabla")
        assert str(e.value) == "geometry blabla field is not present"

    def test_geom(self):
        pass
        # assert isinstance(res, Feature)


class TestBuildFeaturecollection:
    def test_wrong_geom(self):
        geodata_exemple = [
            FakeRowProxy({"geom": None, "test1": "test1", "pom": 1}.items())
        ]
        with pytest.raises(KeyError) as e:
            _build_featurecollection(geodata_exemple, "blabla")
        assert str(e.value) == "geometry blabla field is not present"


class TestToGeojson:
    pass
