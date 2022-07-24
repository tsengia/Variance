from marshmallow import fields
from marshmallow_sqlalchemy import auto_field
from variance.models.muscle import MuscleModel, MuscleGroupModel
from variance.schemas.resource import ResourceBaseSchema

class MuscleSchema(ResourceBaseSchema):
    groups = fields.Nested(lambda: MuscleGroupSchema(only=("id", "canonical_name"), many=True))

    uuid = auto_field(dump_only = True)
    class Meta:
        model = MuscleModel


class MuscleGroupSchema(ResourceBaseSchema):
    muscles = fields.Nested(lambda: MuscleSchema(only=("id", "canonical_name"), many=True))

    uuid = auto_field(dump_only = True)
    class Meta:
        model = MuscleGroupModel
