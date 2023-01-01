from marshmallow_sqlalchemy import auto_field
from variance.models.user_setting import UserSettingModel
from variance.schemas.resource import ResourceBaseSchema
from marshmallow import validate

class UserSettingSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)

    # TODO: Add validation of value against type_hint
    # TODO: Make sure users cannot create new settings
    # TODO: Make sure users cannot change the type_hint of a setting

    type_hint = auto_field(validate=validate.OneOf(\
            ["boolean", "number", "Unit", "string"]\
        ))

    class Meta:
        model = UserSettingModel
