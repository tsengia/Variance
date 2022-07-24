
from variance.models.exercise import ExerciseModel
from variance.schemas.exercise import ExerciseSchema
from variance.api.resource_api import VarianceResource


exercise_endpoint = VarianceResource(ExerciseModel, ExerciseSchema, __name__, "exercises")
