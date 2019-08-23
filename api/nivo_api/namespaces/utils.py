from uuid import UUID

from flask_restplus import fields


class UUIDField(fields.Raw):
    def format(self, value: UUID) -> str:
        return str(value)
