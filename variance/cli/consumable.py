from variance.models.nutrition import ConsumableModel
from variance.schemas.nutrition import ConsumableSchema
from variance.cli.resource import ResourceCLI

consumable_cli = ResourceCLI(ConsumableModel, ConsumableSchema, "Consumables", "consumables")
