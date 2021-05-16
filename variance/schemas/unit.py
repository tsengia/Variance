from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.unit import UnitModel


class UnitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UnitModel
        load_instance = False
