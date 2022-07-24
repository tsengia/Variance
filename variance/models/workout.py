"""
Module for representing and tracking workout plans and entries.
"""
from datetime import datetime

from variance.extensions import db, ResourceBase


class SetEntryModel(ResourceBase):
    """These are sets that have been completed by users"""

    __tablename__ = "SetEntryIndex"

    time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    "Time this set was done/entered"

    exercise_uuid = db.Column(db.String(36), db.ForeignKey(
        "ExerciseIndex.uuid"), nullable=False)
    "ID of the Exercise performed for this Set"
    exercise = db.relationship(
        "ExerciseModel", foreign_keys="SetEntryModel.exercise_uuid")
    "Exercise performed for this Set"

    reps = db.Column(db.Integer, nullable=False, default=1)
    "Number of times this exercise was performed in this set"

    duration = db.Column(db.Float, nullable=True)
    "Duration that this exercise was done for (if it is measured in time)"
    duration_unit_uuid = db.Column(
        db.String(36), db.ForeignKey("UnitIndex.uuid"), nullable=False)
    duration_unit = db.relationship(
        "UnitModel", foreign_keys="SetEntryModel.duration_unit_uuid")

    distance = db.Column(db.Float, nullable=True)
    "Distance that this exercise was done for (if it is measured in distance)"
    distance_unit_uuid = db.Column(
        db.String(36), db.ForeignKey("UnitIndex.uuid"), nullable=False)
    distance_unit = db.relationship(
        "UnitModel", foreign_keys="SetEntryModel.distance_unit_uuid")

    weight = db.Column(db.Float, nullable=True)
    "Weight that this exercise was done with (if this uses weight)"
    weight_unit_uuid = db.Column(
        db.String(36), db.ForeignKey("UnitIndex.uuid"), nullable=False)
    weight_unit = db.relationship(
        "UnitModel", foreign_keys="SetEntryModel.weight_unit_uuid")

    def __str__(self) -> str:
        return "%s SetEntryModel: @%s o%u(%s) e%u(%s) r(%u)" % (self.uuid,
                                                                str(self.time),
                                                                self.owner.uuid,
                                                                self.owner.username,
                                                                self.exercise_uuid,
                                                                self.exercise.name, self.reps)

class SetPlanModel(ResourceBase):
    "These are sets that are planned to be completed by the user in a Workout"
    __tablename__ = "SetPlanIndex"

    # What exercise is being done for this set?
    exercise_uuid = db.Column(db.String(36), db.ForeignKey(
        "ExerciseIndex.uuid"), nullable=False)
    exercise = db.relationship(
        "ExerciseModel", foreign_keys="SetPlanModel.exercise_uuid")
    "The exercises that this set is performing"

    # What workout day does this belond to?
    workout_uuid = db.Column(db.String(36), db.ForeignKey(
        "WorkoutIndex.uuid"), nullable=False)
    workout = db.relationship(
        "WorkoutModel",
        foreign_keys="SetPlanModel.workout_uuid",
        back_populates="sets")
    "The day that this set belongs to in the workout plan"

    order = db.Column(db.Integer, nullable=True)
    "Field for specifying where this set falls."

    reps = db.Column(db.Integer, nullable=False, default=1)
    "Number of times this exercise should be performed in this set."

    duration = db.Column(db.Float, nullable=True)
    "Duration that this exercise should be done with (if it is measured in time)"
    duration_unit_uuid = db.Column(
        db.String(36), db.ForeignKey("UnitIndex.uuid"), nullable=False)
    duration_unit = db.relationship(
        "UnitModel", foreign_keys="SetPlanModel.duration_unit_uuid")

    distance = db.Column(db.Float, nullable=True)
    "Distance that this exercise should be done with (if it is measured in distance)"
    distance_unit_uuid = db.Column(
        db.String(36), db.ForeignKey("UnitIndex.uuid"), nullable=False)
    distance_unit = db.relationship(
        "UnitModel", foreign_keys="SetPlanModel.distance_unit_uuid")

    weight = db.Column(db.Float, nullable=True)
    "Weight that this exercise should be done with (if this uses weight)"
    weight_unit_uuid = db.Column(
        db.String(36), db.ForeignKey("UnitIndex.uuid"), nullable=False)
    weight_unit = db.relationship(
        "UnitModel", foreign_keys="SetPlanModel.weight_unit_uuid")

    # Lambda measures. These are for dynamically generated goals. Aka, 90% of 1 rep max, etc
    # Each lambda function can take a Float parameter and a Tracker parameter.
    duration_lambda_uuid = db.Column(
        db.String(36), db.ForeignKey("LambdaIndex.uuid"), nullable=True)
    duration_lambda = db.relationship(
        "LambdaModel", foreign_keys="SetPlanModel.duration_lambda_uuid")
    duration_lambda_param = db.Column(db.Float, nullable=True)
    duration_lambda_tracker_uuid = db.Column(
        db.String(36), db.ForeignKey("TrackerIndex.uuid"), nullable=True)
    duration_lambda_tracker_param = db.relationship(
        "TrackerModel", foreign_keys="SetPlanModel.duration_lambda_tracker_uuid")

    distance_lambda_uuid = db.Column(
        db.String(36), db.ForeignKey("LambdaIndex.uuid"), nullable=True)
    distance_lambda = db.relationship(
        "LambdaModel", foreign_keys="SetPlanModel.distance_lambda_uuid")
    distance_lambda_param = db.Column(db.Float, nullable=True)
    distance_lambda_tracker_uuid = db.Column(
        db.String(36), db.ForeignKey("TrackerIndex.uuid"), nullable=True)
    distance_lambda_tracker_param = db.relationship(
        "TrackerModel", foreign_keys="SetPlanModel.distance_lambda_tracker_uuid")

    weight_lambda_uuid = db.Column(
        db.String(36), db.ForeignKey("LambdaIndex.uuid"), nullable=True)
    weight_lambda = db.relationship(
        "LambdaModel", foreign_keys="SetPlanModel.weight_lambda_uuid")
    weight_lambda_param = db.Column(db.Float, nullable=True)
    weight_lambda_tracker_uuid = db.Column(
        db.String(36), db.ForeignKey("TrackerIndex.uuid"), nullable=True)
    weight_lambda_tracker_param = db.relationship(
        "TrackerModel", foreign_keys="SetPlanModel.weight_lambda_tracker_uuid")

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
        return "%s SetPlanModel: w%u, %u reps, %u(%s)" % (
            self.uuid, self.workout_uuid, self.reps, self.exercise_uuid, self.exercise.name)


class WorkoutModel(ResourceBase):
    """
    A WorkoutModel (Workout) if a collection of WorkoutSets (sets) that a user plans to complete.
    WorkoutModels can represent a day of the week/month, or can be completely free from being bound to a time/day.
    """
    __tablename__ = "WorkoutIndex"

    name = db.Column(db.String(100), nullable=False)
    "Name of the workout day"

    day = db.Column(db.String(20), nullable=True)
    "What day does this occur on? Freeform entry"

    week = db.Column(db.String(20), nullable=True)
    "What week does this occur on? Freeform entry"

    sets = db.relationship(
        "SetPlanModel", back_populates="workout", cascade="all, delete")
    "Sets of exercises that are performed on this day"

    parent_program_uuid = db.Column(db.String(36), db.ForeignKey(
        "WorkoutProgramIndex.uuid"), nullable=False)
    program = db.relationship("WorkoutProgramModel", back_populates="workouts")
    "Workout Program this workout belongs to"

    def __str__(self) -> str:
        return "%s WorkoutModel: %s on %s, %u" % (
            self.uuid, self.name, self.day, self.week_uuid)


class WorkoutProgramModel(ResourceBase):
    """
    A WorkoutProgram is a collection of Workouts created by a user.
    These Workouts can be sequential (ie. one for each day of the week/month), or they can be non-sequential.
    """
    __tablename__ = "WorkoutProgramIndex"

    name = db.Column(db.String(100), nullable=False)
    "Display name of the workout program"

    description = db.Column(db.String(300), nullable=True)
    "Description of the workout program"

    workouts = db.relationship(
        "WorkoutModel", back_populates="program", cascade="all, delete")
    "Workouts in this program"

    def __str__(self) -> str:
        return "%s ProgramModel: %s, %u(%s), public(%s)" % (
            self.uuid, self.name, self.owner_uuid, self.owner.username, str(self.is_public))
