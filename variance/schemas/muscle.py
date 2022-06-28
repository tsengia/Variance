from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.muscle import MuscleModel, MuscleGroupModel


class MuscleSchema(SQLAlchemyAutoSchema):
    groups = fields.Nested(lambda: MuscleGroupSchema(only=("id", "canonical_name"), many=True))

    class Meta:
        model = MuscleModel
        load_instance = False


class MuscleGroupSchema(SQLAlchemyAutoSchema):
    muscles = fields.Nested(lambda: MuscleSchema(only=("id", "canonical_name"), many=True))

    class Meta:
        model = MuscleGroupModel
        load_instance = False
