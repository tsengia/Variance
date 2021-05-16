from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.exercise import ExerciseModel


class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ExerciseModel
        load_instance = False
