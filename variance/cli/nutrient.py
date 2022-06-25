from variance.models.nutrition import NutrientInfoModel
from variance.schemas.nutrition import NutrientInfoSchema
from variance.cli.resource import ResourceCLI

nutrient_cli = ResourceCLI(NutrientInfoModel, NutrientInfoSchema, "NutrientInfo", "nutrients")
