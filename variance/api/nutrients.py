from variance.models.nutrition import NutrientInfoModel
from variance.schemas.nutrition import NutrientInfoSchema
from variance.api.resource_api import VarianceResource

nutrient_info_endpoint = VarianceResource(NutrientInfoModel, NutrientInfoSchema, __name__, "nutrients")
