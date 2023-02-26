
from variance.models.exercise import ExerciseModel
from variance.schemas.exercise import ExerciseSchema
from variance.api.resource_api import VarianceCollection

exercises_endpoint = VarianceCollection(ExerciseModel, ExerciseSchema, __name__, "exercises")
