from marshmallow_sqlalchemy import auto_field
from variance.models.global_setting import GlobalSettingModel
from variance.schemas.resource import ResourceBaseSchema
from marshmallow import validate

class GlobalSettingSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)

    # TODO: Add validation of value against type_hint

    type_hint = auto_field(validate=validate.OneOf(\
            ["boolean", "number", "Unit", "string"]\
        ))

    class Meta:
        model = GlobalSettingModel
