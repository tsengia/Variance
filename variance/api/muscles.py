from variance.models.muscle import MuscleModel, MuscleGroupModel
from variance.schemas.muscle import MuscleSchema, MuscleGroupSchema
from variance.api.resource_api import VarianceResource

muscle_endpoint = VarianceResource(MuscleModel, MuscleSchema, "muscles", "muscle")
muscle_groups_endpoint = VarianceResource(MuscleGroupModel, MuscleGroupSchema, "muscles_groups", "groups")
muscle_groups_endpoint.set_parent(muscle_endpoint)