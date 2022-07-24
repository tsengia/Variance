from marshmallow_sqlalchemy import auto_field
from variance.models.gym import GymModel
from variance.schemas.resource import ResourceBaseSchema

class GymSchema(ResourceBaseSchema):
    class Meta:
        model = GymModel

    uuid = auto_field(dump_only=True)
