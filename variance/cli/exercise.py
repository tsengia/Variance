from pathlib import Path
import click
from flask.cli import AppGroup

from variance.models.exercise import ExerciseModel
from variance.schemas.exercise import ExerciseSchema

exercise_cli = ResourceCLI(ExerciseModel, ExerciseSchema, "Exercises", "exercises", ("id", ))
