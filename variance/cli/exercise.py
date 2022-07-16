from variance.models.exercise import ExerciseModel
from variance.schemas.exercise import ExerciseSchema
from variance.cli.resource import ResourceCLI

exercise_cli = ResourceCLI(ExerciseModel, ExerciseSchema, "Exercises", "exercises", ("id", ))
