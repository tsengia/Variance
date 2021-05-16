from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.muscle import MuscleModel, MuscleGroupModel


class MuscleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MuscleModel
        load_instance = False


class MuscleGroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MuscleGroupModel
        load_instance = False
