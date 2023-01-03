import re

from marshmallow_sqlalchemy import auto_field
from variance.models.global_setting import GlobalSettingModel
from variance.models.unit import UnitModel
from variance.schemas.resource import ResourceBaseSchema
from marshmallow import validate, ValidationError, validates_schema, fields

import click

NUMBER_REGEX = re.compile("^[-]?[0-9]+(\.[0-9]+)?")

def parse_setting_value(setting):
    print(setting)
    t = setting["type_hint"]
    v = setting["value"]
    if t == "boolean":
        return v == "True"
    elif t == "string":
        return str(v)
    elif t == "float":
        return float(v)
    elif t == "Unit":
        return UnitModel.get(UnitModel.get_uuid_by_abbreviation(v))

class GlobalSettingSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    value = auto_field()

    type_hint = auto_field(validate=validate.OneOf(\
            ["boolean", "float", "Unit", "string"]\
        ))

    @validates_schema(skip_on_field_errors=True, pass_many=False)
    def validate_value_against_type(self, data, partial, many):
        t = data["type_hint"]
        v = data["value"]
        if t == "boolean":
            if (not v == "True") and (not v == "False"):
                raise ValidationError("value is not a boolean! type_hint is set to 'boolean'.", field_name="value")
        if t == "float":
            if not NUMBER_REGEX.match(v):
                raise ValidationError("value is not a number! type_hint is set to 'float'.", field_name="value")
        if t == "Unit":
            if not UnitModel.get_uuid_by_abbreviation(v):
                raise ValidationError("value is not a unit abbreviation! type_hint is set to 'Unit'. Are you sure the unit %s exists?" % v, field_name="value")

    class Meta:
        model = GlobalSettingModel
