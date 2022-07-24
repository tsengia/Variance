from marshmallow_sqlalchemy import auto_field
from variance.models.unit import UnitModel
from variance.schemas.resource import ResourceBaseSchema

class UnitSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)

    class Meta:
        model = UnitModel
