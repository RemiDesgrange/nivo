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

    def get(self, con: Connection, entity_id: UUID = None, fields: List[Column] = None) -> Union[
        List[RowProxy], RowProxy]:
        fields = fields if fields else self.columns
        req = select(fields).where(self._get_pk() == entity_id) if entity_id else select(fields)
        res = con.execute(req).fetchall()
        if len(res) == 1:
            return res[0]
        else:
            return res


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
                cols.append(func.ST_AsGeoJson(self._the_geom()).label(c.name).cast(JSON))
            else:
                cols.append(c)
        return cols

    def get_geojson(self, con: Connection, entity_id: UUID = None) -> Dict:
        fields = self._replace_geom_column()
        res = self.get(con, entity_id, fields)
        return to_geojson(res)
