from variance.models.nutrition import ConsumableModel
from variance.schemas.nutrition import ConsumableSchema
from variance.api.resource_api import VarianceResource

consumable_endpoint = VarianceResource(ConsumableModel, ConsumableSchema, __name__, "consumable")
