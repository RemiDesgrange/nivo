# https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#using-enum-with-array
import re
from xml import etree

import sqlalchemy as sa
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import ARRAY


class ArrayOfEnum(TypeDecorator):
    impl = ARRAY

    def bind_expression(self, bindvalue):
        return sa.cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfEnum, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            inner = re.match(r"^{(.*)}$", value).group(1)
            return inner.split(",") if inner else []

        def process(value):
            if value is None:
                return None
            return super_rp(handle_raw_string(value))

        return process


# sqlalchemy doesn't have XML type. Need to implement it.
class XML(sa.types.UserDefinedType):
    def get_col_spec(self):
        return "XML"

    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                if isinstance(value, str):
                    return value
                else:
                    return etree.tostring(value)
            else:
                return None

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                value = etree.fromstring(value)
            return value

        return process
