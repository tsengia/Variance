from variance.models.unit import UnitModel
from variance.schemas.unit import UnitSchema
from variance.cli.resource import ResourceCLI

unit_cli = ResourceCLI(UnitModel, UnitSchema, "Units", "units")
