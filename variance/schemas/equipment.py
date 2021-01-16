from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.equipment import EquipmentModel

class EquipmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EquipmentModel
        load_instance = False