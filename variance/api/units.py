from variance.models.unit import UnitModel
from variance.schemas.unit import UnitSchema
from variance.api.resource_api import VarianceCollection

units_endpoint = VarianceCollection(UnitModel, UnitSchema, __name__, "units")
