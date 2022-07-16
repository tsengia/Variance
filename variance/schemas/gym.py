from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.gym import GymModel

class GymSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GymModel
        load_instance = False
