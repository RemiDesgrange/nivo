from typing import List, Union

import feedparser

from nivo_api.core.api_schema.geojson import FeatureCollection
from nivo_api.namespaces.flowcapt import flowcapt_api

flowcapt_api.add_model("FeatureCollection", FeatureCollection)


class FlowCaptRssToJSON:
    """
    JSON from isaw is broken
    """

    def __init__(self, url: str) -> None:
        self.url = url

    def __call__(self, *args, **kwargs) -> dict:
        req = feedparser.parse(self.url)
        try:
            data = self._parse_headers(req["feed"])
            measures = self._parse_measures(req["entries"])
            data["measures"] = measures
            return data
        except KeyError:
            raise AssertionError("Wrong data source, cannot parse data")

    def _parse_measures(self, entries: list) -> dict:
        measures = dict()
        for entry in entries:
            measures[entry["title"]] = self._parse_numeric(entry["data"].split(","))
        return measures

    def _parse_headers(self, feed: dict) -> dict:
        return {
            "station": feed["title"],
            "url": feed["link"],
            "description": feed["subtitle"],
            "lastdata": feed["lastdata"],
            "generation": feed["generation"],
            "generator": feed["generator"],
        }

    def _parse_numeric(self, data: List[str]) -> List[Union[float, int]]:
        parsed_data = []
        for d in data:
            if not d:
                continue
            try:
                x = int(d)
            except ValueError:
                x = float(d)
            parsed_data.append(x)
        return parsed_data
