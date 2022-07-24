
from marshmallow_sqlalchemy import auto_field
from variance.models.workout import SetEntryModel, SetPlanModel, WorkoutModel, WorkoutProgramModel
from variance.schemas.resource import ResourceBaseSchema

class SetEntrySchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = SetEntryModel

class SetPlanSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = SetPlanModel

class WorkoutSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = WorkoutModel

class WorkoutProgramSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = WorkoutProgramModel
