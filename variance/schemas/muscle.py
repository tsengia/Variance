from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.muscle import MuscleModel, MuscleGroupModel


class MuscleSchema(SQLAlchemyAutoSchema):
    groups = fields.List(fields.Nested(lambda: MuscleGroupSchema(only=("id", "canonical_name"))))

    class Meta:
        model = MuscleModel
        load_instance = False


class MuscleGroupSchema(SQLAlchemyAutoSchema):
    muscles = fields.List(fields.Nested(lambda: MuscleSchema(only=("id", "canonical_name"))))

    class Meta:
        model = MuscleGroupModel
        load_instance = False
