from variance.models.muscle import MuscleModel, MuscleGroupModel
from variance.schemas.muscle import MuscleSchema, MuscleGroupSchema
from variance.api.resource_api import VarianceCollection

muscle_endpoint = VarianceCollection(MuscleModel, MuscleSchema, "muscles", "muscle")
muscle_groups_endpoint = VarianceCollection(MuscleGroupModel, MuscleGroupSchema, "muscle_groups", "muscle/group")