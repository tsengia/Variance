from variance.models.unit import UnitModel
from variance.schemas.unit import UnitSchema
from variance.api.resource_api import VarianceResource

units_endpoint = VarianceResource(UnitModel, UnitSchema, __name__, "units")
