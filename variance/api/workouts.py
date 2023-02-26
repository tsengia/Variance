
from variance.models.workout import SetEntryModel, SetPlanModel, WorkoutModel, WorkoutProgramModel
from variance.schemas.workout import SetEntrySchema, SetPlanSchema, WorkoutSchema, WorkoutProgramSchema
from variance.api.resource_api import VarianceCollection, VarianceChildResource

workout_programs_endpoint = VarianceCollection(WorkoutProgramModel, WorkoutProgramSchema, "workout_programs", "workouts")
