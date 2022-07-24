from variance.schemas.resource import ResourceBaseSchema
from variance.models.exercise import ExerciseModel

from marshmallow_sqlalchemy import auto_field

class ExerciseSchema(ResourceBaseSchema):
    class Meta:
        model = ExerciseModel

    uuid = auto_field(dump_only=True)
