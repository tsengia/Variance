from variance.models.nutrition import NutrientInfoModel
from variance.schemas.nutrition import NutrientInfoSchema
from variance.api.resource_api import VarianceCollection

nutrient_info_endpoint = VarianceCollection(NutrientInfoModel, NutrientInfoSchema, __name__, "nutrients")
