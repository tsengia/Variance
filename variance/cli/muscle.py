from variance.models.muscle import MuscleModel, MuscleGroupModel
from variance.schemas.muscle import MuscleSchema, MuscleGroupSchema
from variance.cli.resource import ResourceCLI

muscle_cli = ResourceCLI(MuscleModel, MuscleSchema, "Muscles", "muscles", ("groups",))
muscle_group_cli = ResourceCLI(MuscleGroupModel, MuscleGroupSchema, "MuscleGroups", "groups", ("muscles.uuid",))
muscle_group_cli.attach(muscle_cli.group)
