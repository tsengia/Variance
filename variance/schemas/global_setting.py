import re

from marshmallow_sqlalchemy import auto_field
from variance.models.global_setting import GlobalSettingModel
from variance.models.unit import UnitModel
from variance.schemas.resource import ResourceBaseSchema
from marshmallow import validate, ValidationError

import click

VALID_BOOLEAN_TRUE = ["TRUE", "True", "true", "1", "yes", "YES", "Yes"]
VALID_BOOLEAN_FALSE = ["FALSE", "False", "false", "0", "no", "NO", "No"]
VALID_BOOLEAN = [*VALID_BOOLEAN_TRUE, *VALID_BOOLEAN_FALSE]

NUMBER_REGEX = re.compile("^[-][0-9]+(\.[0-9]+)?")

class GlobalSettingSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)

    # TODO: Add validation of value against type_hint

    type_hint = auto_field(validate=validate.OneOf(\
            ["boolean", "number", "Unit", "string"]\
        ))

    def validate(self, data, *, session=None, **kwargs):
        super().validate(data, session=session, **kwargs)
        t = kwargs["type_hint"]
        v = kwargs["value"]
        if t == "boolean":
            if v not in VALID_BOOLEAN:
                raise ValidationError("value is not a boolean! type_hint is set to 'boolean'.", field_name="value")
        if t == "number":
            if not NUMBER_REGEX.match(v):
                raise ValidationError("value is not a number! type_hint is set to 'number'.", field_name="value")
        if t == "Unit":
            if not UnitModel.get_uuid_by_abbreviation(v):
                raise ValidationError("value is not a unit abbreviation! type_hint is set to 'Unit'. Are you sure the unit %s exists?" % v, field_name="value")

    class Meta:
        model = GlobalSettingModel
