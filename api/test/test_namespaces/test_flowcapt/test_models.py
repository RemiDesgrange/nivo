import pytest

from nivo_api.namespaces.flowcapt.models import FlowCaptRssToJSON


class TestFlowCaptRssToJSON:
    def test_non_valid_url(self):
        f = FlowCaptRssToJSON("toto_titi")
        with pytest.raises(AssertionError) as a:
            f()
            assert a.value == "Wrong data source, cannot parse data"

    def test_non_valid_schema(self):
        f = FlowCaptRssToJSON("http://localhost/test.rss")
        with pytest.raises(AssertionError) as a:
            f()
            assert a.value == "Wrong data source, cannot parse data"

    def test_no_data(self):
        # Website that is not returning rss
        f = FlowCaptRssToJSON("https://google.com")
        with pytest.raises(AssertionError) as a:
            f()
            assert a.value == "Fail to query https://google.com"

    def test_correct_url_wrong_data(self):
        f = FlowCaptRssToJSON("https://www.lemonde.fr/rss/une.xml")
        with pytest.raises(AssertionError) as a:
            f()
            assert a.value == "Wrong data source, cannot parse data"

    def test_correct_data(self):
        # ok relying on a distant service is not right, I should mock it...

        f = FlowCaptRssToJSON("http://www.isaw.ch/idod/idod.php?&f=rss&d=1&s=FGIE1")
        res = f()
        assert res["station"] == "FGIE1"
