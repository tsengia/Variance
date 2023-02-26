from variance.models.nutrition import ConsumableModel
from variance.schemas.nutrition import ConsumableSchema
from variance.api.resource_api import VarianceCollection

consumable_endpoint = VarianceCollection(ConsumableModel, ConsumableSchema, __name__, "consumable")
