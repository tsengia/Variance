from marshmallow import Schema, fields, ValidationError, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.unit import UnitModel

import re

unit_name_schema = re.compile("^[a-zA-Z0-9_-]{1,21}$")

class UnitIDSchema(Schema):
    id = fields.Integer(required=True)

class UnitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UnitModel
        load_instance = False
