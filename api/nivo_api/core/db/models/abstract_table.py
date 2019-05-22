from typing import List, Union, Dict
from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import Table, select, Column, func, JSON
from sqlalchemy.engine import RowProxy, Connection

from nivo_api.core.db.helpers import to_geojson


class AbstractTable(Table):
    def _get_pk(self) -> Column:
        """assume only one PK !"""
        pk = list(self.primary_key.columns)
        return pk.pop()

    def get(self, con: Connection, entity_id: UUID = None, fields: List[Column] = None, limit: int = 500) -> Union[
        List[RowProxy], RowProxy]:
        """
        return a list of rows or a row if the entity_id (the pk) is not null. limit to 500 rows max by default to avoid
        problems
        """
        fields = fields if fields else self.columns
        req = select(fields).where(self._get_pk() == entity_id) if entity_id else select(fields)
        res = con.execute(req.limit(limit)).fetchall()
        if len(res) == 1:
            return res[0]
        else:
            return res

    def get_json(self, con, entity_id: UUID = None, fields: List[Column] = None, limit: int = 500) -> Union[Dict, List[Dict]]:
        res = self.get(con, entity_id, fields, limit)
        if isinstance(res, RowProxy):
            return dict(res)
        else:
            return list(map(lambda x: dict(x), res))


class AbstractSpatialTable(AbstractTable):

    def _the_geom(self) -> Column:
        for x in self.columns:
            if isinstance(x.type, Geometry):
                return x

    def _replace_geom_column(self) -> List[Column]:
        """
        Replace the geom column by a geojson one.
        :return:
        """
        cols = list()
        for c in self.columns:
            if isinstance(c.type, Geometry):
                cols.append(func.ST_AsGeoJson(self._the_geom()).cast(JSON).label(c.name))
            else:
                cols.append(c)
        return cols

    def get_geojson(self, con: Connection, entity_id: UUID = None) -> Dict:
        fields = self._replace_geom_column()
        res = self.get(con, entity_id, fields)
        return to_geojson(res)
