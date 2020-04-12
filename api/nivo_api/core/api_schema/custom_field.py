from flask_restx import fields


class UUID(fields.Raw):
    def format(self, value):
        return str(value)
