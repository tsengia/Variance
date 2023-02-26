from variance.models.equipment import EquipmentModel
from variance.schemas.equipment import EquipmentSchema
from variance.api.resource_api import VarianceCollection

equipment_endpoint = VarianceCollection(EquipmentModel, EquipmentSchema, __name__, "equipment")
