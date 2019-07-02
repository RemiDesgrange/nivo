from flask_restplus import fields


class UUID(fields.Raw):
    def format(self, value):
        return str(value)
