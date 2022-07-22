"""
Module for representing and tracking workout plans and entries.
"""
from datetime import datetime

from variance.extensions import db


class SetEntryModel(db.Model):
    """These are sets that have been completed by users"""

    __tablename__ = "SetEntryIndex"

    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    "Time this set was done/entered"

    exercise_id = db.Column(db.Integer, db.ForeignKey(
        "ExerciseIndex.id"), nullable=False)
    "ID of the Exercise performed for this Set"
    exercise = db.relationship(
        "ExerciseModel", foreign_keys="SetEntryModel.exercise_id")
    "Exercise performed for this Set"

    reps = db.Column(db.Integer, nullable=False, default=1)
    "Number of times this exercise was performed in this set"

    duration = db.Column(db.Float, nullable=True)
    "Duration that this exercise was done for (if it is measured in time)"
    duration_unit_id = db.Column(
        db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    duration_unit = db.relationship(
        "UnitModel", foreign_keys="SetEntryModel.duration_unit_id")

    distance = db.Column(db.Float, nullable=True)
    "Distance that this exercise was done for (if it is measured in distance)"
    distance_unit_id = db.Column(
        db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    distance_unit = db.relationship(
        "UnitModel", foreign_keys="SetEntryModel.distance_unit_id")

    weight = db.Column(db.Float, nullable=True)
    "Weight that this exercise was done with (if this uses weight)"
    weight_unit_id = db.Column(
        db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    weight_unit = db.relationship(
        "UnitModel", foreign_keys="SetEntryModel.weight_unit_id")

    def __str__(self) -> str:
        return "%u SetEntryModel: @%s o%u(%s) e%u(%s) r(%u)" % (self.id,
                                                                str(self.time),
                                                                self.owner.id,
                                                                self.owner.username,
                                                                self.exercise_id,
                                                                self.exercise.name, self.reps)

class SetPlanModel(db.Model):
    "These are sets that are planned to be completed by the user in a Workout"
    __tablename__ = "SetPlanIndex"

    id = db.Column(db.Integer, primary_key=True)

    # What exercise is being done for this set?
    exercise_id = db.Column(db.Integer, db.ForeignKey(
        "ExerciseIndex.id"), nullable=False)
    exercise = db.relationship(
        "ExerciseModel", foreign_keys="SetPlanModel.exercise_id")
    "The exercises that this set is performing"

    # What workout day does this belond to?
    workout_id = db.Column(db.Integer, db.ForeignKey(
        "WorkoutIndex.id"), nullable=False)
    workout = db.relationship(
        "WorkoutModel",
        foreign_keys="SetPlanModel.workout_id",
        back_populates="sets")
    "The day that this set belongs to in the workout plan"

    order = db.Column(db.Integer, nullable=True)
    "Field for specifying where this set falls."

    reps = db.Column(db.Integer, nullable=False, default=1)
    "Number of times this exercise should be performed in this set."

    duration = db.Column(db.Float, nullable=True)
    "Duration that this exercise should be done with (if it is measured in time)"
    duration_unit_id = db.Column(
        db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    duration_unit = db.relationship(
        "UnitModel", foreign_keys="SetPlanModel.duration_unit_id")

    distance = db.Column(db.Float, nullable=True)
    "Distance that this exercise should be done with (if it is measured in distance)"
    distance_unit_id = db.Column(
        db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    distance_unit = db.relationship(
        "UnitModel", foreign_keys="SetPlanModel.distance_unit_id")

    weight = db.Column(db.Float, nullable=True)
    "Weight that this exercise should be done with (if this uses weight)"
    weight_unit_id = db.Column(
        db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    weight_unit = db.relationship(
        "UnitModel", foreign_keys="SetPlanModel.weight_unit_id")

    # Lambda measures. These are for dynamically generated goals. Aka, 90% of 1 rep max, etc
    # Each lambda function can take a Float parameter and a Tracker parameter.
    duration_lambda_id = db.Column(
        db.Integer, db.ForeignKey("LambdaIndex.id"), nullable=True)
    duration_lambda = db.relationship(
        "LambdaModel", foreign_keys="SetPlanModel.duration_lambda_id")
    duration_lambda_param = db.Column(db.Float, nullable=True)
    duration_lambda_tracker_id = db.Column(
        db.Integer, db.ForeignKey("TrackerIndex.id"), nullable=True)
    duration_lambda_tracker_param = db.relationship(
        "TrackerModel", foreign_keys="SetPlanModel.duration_lambda_tracker_id")

    distance_lambda_id = db.Column(
        db.Integer, db.ForeignKey("LambdaIndex.id"), nullable=True)
    distance_lambda = db.relationship(
        "LambdaModel", foreign_keys="SetPlanModel.distance_lambda_id")
    distance_lambda_param = db.Column(db.Float, nullable=True)
    distance_lambda_tracker_id = db.Column(
        db.Integer, db.ForeignKey("TrackerIndex.id"), nullable=True)
    distance_lambda_tracker_param = db.relationship(
        "TrackerModel", foreign_keys="SetPlanModel.distance_lambda_tracker_id")

    weight_lambda_id = db.Column(
        db.Integer, db.ForeignKey("LambdaIndex.id"), nullable=True)
    weight_lambda = db.relationship(
        "LambdaModel", foreign_keys="SetPlanModel.weight_lambda_id")
    weight_lambda_param = db.Column(db.Float, nullable=True)
    weight_lambda_tracker_id = db.Column(
        db.Integer, db.ForeignKey("TrackerIndex.id"), nullable=True)
    weight_lambda_tracker_param = db.relationship(
        "TrackerModel", foreign_keys="SetPlanModel.weight_lambda_tracker_id")

    def get_weight(self) -> float:
        "TODO: Implement this, should return the weight either from value or lambda"
        return 0.0

    def get_duration(self) -> float:
        "TODO: Implement this, should return the duration either from value or lambda"
        return 0.0

    def get_distance(self) -> float:
        "TODO: Implement this, should return the distance either from value or lambda" 
        return 0.0

    def __str__(self):
        return "%u SetPlanModel: w%u, %u reps, %u(%s)" % (
            self.id, self.workout_id, self.reps, self.exercise_id, self.exercise.name)


class WorkoutModel(db.Model):
    """
    A WorkoutModel (Workout) if a collection of WorkoutSets (sets) that a user plans to complete.
    WorkoutModels can represent a day of the week/month, or can be completely free from being bound to a time/day.
    """
    __tablename__ = "WorkoutIndex"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    "Name of the workout day"

    day = db.Column(db.String(20), nullable=True)
    "What day does this occur on? Freeform entry"

    week = db.Column(db.String(20), nullable=True)
    "What week does this occur on? Freeform entry"

    sets = db.relationship(
        "SetPlanModel", back_populates="workout", cascade="all, delete")
    "Sets of exercises that are performed on this day"

    parent_program_id = db.Column(db.Integer, db.ForeignKey(
        "WorkoutProgramIndex.id"), nullable=False)
    program = db.relationship("WorkoutProgramModel", back_populates="workouts")
    "Workout Program this workout belongs to"

    def __str__(self) -> str:
        return "%u WorkoutModel: %s on %s, %u" % (
            self.id, self.name, self.day, self.week_id)


class WorkoutProgramModel(db.Model):
    """
    A WorkoutProgram is a collection of Workouts created by a user.
    These Workouts can be sequential (ie. one for each day of the week/month), or they can be non-sequential.
    """
    __tablename__ = "WorkoutProgramIndex"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    "Display name of the workout program"

    description = db.Column(db.String(300), nullable=True)
    "Description of the workout program"

    workouts = db.relationship(
        "WorkoutModel", back_populates="program", cascade="all, delete")
    "Workouts in this program"

    def __str__(self) -> str:
        return "%u ProgramModel: %s, %u(%s), public(%s)" % (
            self.id, self.name, self.owner_id, self.owner.username, str(self.is_public))
