from variance.models.gym import GymModel
from variance.schemas.gym import GymSchema
from variance.cli.resource import ResourceCLI

gym_cli = ResourceCLI(GymModel, GymSchema, "Gyms", "gyms", ("id",))
