"""
This module adds the association between Exercises and the Muscles worked
by each exercise.

The association is added outside of the Model definitions for better
decoupling of data.

Importing this file will add the association to each model.
"""
from variance.models.exercise import ExerciseModel
from variance.models.muscle import MuscleModel
from variance.extensions import db


# Define our association table
"""
This association table maps exercises to the collection of muscles
that the exercise targets. The "intensity" column is a relative measure
of how much a muscle is worked by the exercise that should vary from 0 to 1
"""
ExerciseMuscleAssociation= db.Table(
    "ExerciseMuscleAssociation",
    db.metadata,
    db.Column("exercise_id", db.ForeignKey("ExerciseIndex.id")),
    db.Column("muscle_id", db.ForeignKey("MuscleIndex.id")),
    db.Column("intensity", db.Float(), nullable=False)
)

if not hasattr(ExerciseModel, "muscles"):
    # Attach the association to the ExerciseModel
    ExerciseModel.muscles = db.relationship(MuscleModel,
        secondary="ExerciseMuscleAssociation",
        backref="exercises")

if not hasattr(MuscleModel, "exercises"):
    # Attach the association to the MuscleModel
    MuscleModel.exercises = db.relationship(ExerciseModel, 
        secondary="ExerciseMuscleAssociation",
        backref="muscles")

