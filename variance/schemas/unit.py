from marshmallow import Schema, fields, ValidationError, validates

import re

unit_name_schema = re.compile("^[a-zA-Z0-9_-]{1,21}$")

class UnitSchema(Schema):
    name = fields.String(required=True)
    abbreviation = fields.String(required=True)
    dimension = fields.String(required=True)
    multiplier = fields.Float(required=True)

    # TODO: Add validator methods to check name, abbreviation, and dimension
    # TODO: Add load_only and dump_only fields.
