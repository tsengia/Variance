from marshmallow import Schema, fields, ValidationError, validates

class StatusSchema(Schema):
    status = fields.String(required=True)
