from marshmallow_sqlalchemy import auto_field
from variance.models.equipment import EquipmentModel
from variance.schemas.resource import ResourceBaseSchema

class EquipmentSchema(ResourceBaseSchema):

    class Meta:
        model = EquipmentModel
    
    uuid = auto_field(dump_only=True)
