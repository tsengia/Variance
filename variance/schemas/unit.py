from marshmallow import Schema, fields, ValidationError, validates

import re

unit_name_schema = re.compile("^[a-zA-Z0-9_-]{1,21}$")

class UnitIDSchema(Schema):
    id = fields.Integer(required=True)

class UnitSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    name = fields.String(required=True)
    abbreviation = fields.String(required=True)
    dimension = fields.String(required=True)
    multiplier = fields.Float(required=True)

    # TODO: Add validator methods to check name, abbreviation, and dimension
