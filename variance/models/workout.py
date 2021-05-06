from datetime import datetime

from variance import db 

# These are sets that have been completed by users
class SetEntryModel(db.Model):
    __tablename__ = "SetEntryIndex"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Time this set was done/entered
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Exercise performed for this Set
    exercise_id = db.Column(db.Integer, db.ForeignKey("ExerciseIndex.id"), nullable=False)
    exercise = db.relationship("ExerciseModel", foreign_keys="SetEntryModel.exercise_id")
    
    # Number of times this exercise was performed in this set
    reps = db.Column(db.Integer, nullable=False, default=1)
    
    # Duration that this exercise was done for (if it is measured in time)
    duration = db.Column(db.Float, nullable=True)
    duration_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    duration_unit = db.relationship("UnitModel", foreign_keys="SetEntryModel.duration_unit_id")
    
    # Distance that this exercise was done for (if it is measured in distance)
    distance = db.Column(db.Float, nullable=True)
    distance_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    distance_unit = db.relationship("UnitModel", foreign_keys="SetEntryModel.distance_unit_id")
    
    # Weight that this exercise was done with (if this uses weight)
    weight = db.Column(db.Float, nullable=True)
    weight_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    weight_unit = db.relationship("UnitModel", foreign_keys="SetEntryModel.weight_unit_id")

    owner_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", foreign_keys="SetEntryModel.owner_id", back_populates="set_entries")

    @staticmethod
    def has_owner(self):
        return True

    # Returns True is the given user id is considered the owner of this set entry
    def check_owner(self, id):
        return self.owner_id == id

    def __str__(self):
        return "%u SetEntryModel: @%s o%u(%s) e%u(%s) r(%u)" % (self.id, str(self.time), self.owner.id, self.owner.username, self.exercise_id, self.exercise.name. self.reps)
    
# Theses are sets that are planned to be completed (in a workout plan)
class SetPlanModel(db.Model):
    __tablename__ = "SetPlanIndex"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # What exercise is being done for this set?
    exercise_id = db.Column(db.Integer, db.ForeignKey("ExerciseIndex.id"), nullable=False)
    exercise = db.relationship("ExerciseModel", foreign_keys="SetPlanModel.exercise_id")
    
    # What workout day does this belond to?
    workout_id = db.Column(db.Integer, db.ForeignKey("WorkoutIndex.id"), nullable=False)
    workout = db.relationship("WorkoutModel", foreign_keys="SetPlanModel.workout_id", back_populates="sets")
    
    # Field for specifying where this set falls.
    order = db.Column(db.Integer, nullable=True)
    
    # Number of times this exercise was performed in this set
    reps = db.Column(db.Integer, nullable=False, default=1)
    
    # Duration that this exercise was done for (if it is measured in time)
    duration = db.Column(db.Float, nullable=True)
    duration_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    duration_unit = db.relationship("UnitModel", foreign_keys="SetPlanModel.duration_unit_id")
    
    # Distance that this exercise was done for (if it is measured in distance)
    distance = db.Column(db.Float, nullable=True)
    distance_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    distance_unit = db.relationship("UnitModel", foreign_keys="SetPlanModel.distance_unit_id")
    
    # Weight that this exercise was done with (if this uses weight)
    weight = db.Column(db.Float, nullable=True)
    weight_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    weight_unit = db.relationship("UnitModel", foreign_keys="SetPlanModel.weight_unit_id")

    # Lambda measures. These are for dynamically generated goals. Aka, 90% of 1 rep max, etc
    # Each lambda function can take a Float parameter and a Tracker parameter.
    duration_lambda_id = db.Column(db.Integer, db.ForeignKey("LambdaIndex.id"), nullable=True)
    duration_lambda = db.relationship("LambdaModel", foreign_keys="SetPlanModel.duration_lambda_id")
    duration_lambda_param = db.Column(db.Float, nullable=True)
    duration_lambda_tracker_id = db.Column(db.Integer, db.ForeignKey("TrackerIndex.id"), nullable=True)
    duration_lambda_tracker_param = db.relationship("TrackerModel", foreign_keys="SetPlanModel.duration_lambda_tracker_id")

    distance_lambda_id = db.Column(db.Integer, db.ForeignKey("LambdaIndex.id"), nullable=True)
    distance_lambda = db.relationship("LambdaModel", foreign_keys="SetPlanModel.distance_lambda_id")
    distance_lambda_param = db.Column(db.Float, nullable=True)
    distance_lambda_tracker_id = db.Column(db.Integer, db.ForeignKey("TrackerIndex.id"), nullable=True)
    distance_lambda_tracker_param = db.relationship("TrackerModel", foreign_keys="SetPlanModel.distance_lambda_tracker_id")

    weight_lambda_id = db.Column(db.Integer, db.ForeignKey("LambdaIndex.id"), nullable=True)
    weight_lambda = db.relationship("LambdaModel", foreign_keys="SetPlanModel.weight_lambda_id")
    weight_lambda_param = db.Column(db.Float, nullable=True)
    weight_lambda_tracker_id = db.Column(db.Integer, db.ForeignKey("TrackerIndex.id"), nullable=True)
    weight_lambda_tracker_param = db.relationship("TrackerModel", foreign_keys="SetPlanModel.weight_lambda_tracker_id")


    def get_weight(self):
        return 0 # TODO: Implement this, should return the weight either from value or lambda

    def get_duration(self):
        return 0 # TODO: Implement this, should return the weight either from value or lambda

    def get_distance(self):
        return 0 # TODO: Implement this, should return the weight either from value or lambda

    @staticmethod
    def has_owner(self):
        return True
        
    # Returns True is the given user id is considered the owner of this tracker entry
    def check_owner(self, id):
        return self.workout.check_owner(id)
        
    def __str__(self):
        return "%u SetPlanModel: w%u, %u reps, %u(%s)" % (self.id, self.workout_id, self.reps, self.exercise_id, self.exercise.name)

class WorkoutModel(db.Model):
    __tablename__ = "WorkoutIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the workout day
    name = db.Column(db.String(100), nullable=False)

    # What day does this occur on? Freeform entry
    day = db.Column(db.String(20), nullable=True)

    # What week does this occur on? Freeform entry
    week = db.Column(db.String(20), nullable=True)

    # Sets of exercises that are performed on this day
    sets = db.relationship("SetPlanModel", back_populates="workout", cascade="all, delete")

    # Workout Program this workout belongs to
    parent_program_id = db.Column(db.Integer, db.ForeignKey("WorkoutProgramIndex.id"), nullable=False)
    program = db.relationship("WorkoutProgramModel", back_populates="workouts")

    @staticmethod
    def has_owner(self):
        return True

    # Returns True is the given user id is considered the owner of this tracker entry
    def check_owner(self, id):
        return self.program.check_owner(id)

    def __str__(self):
        return "%u WorkoutModel: %s on %s, %u" % (self.id, self.name, self.day, self.week_id)

class WorkoutProgramModel(db.Model):
    __tablename__ = "WorkoutProgramIndex"
    
    id = db.Column(db.Integer, primary_key=True)

    # Name of the workout program
    name = db.Column(db.String(100), nullable=False)
    
    # Description of the workout program
    description = db.Column(db.String(300), nullable=True)
    
    # Can other users see this workout program?
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    
    # User who owns this program
    owner_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", back_populates="programs")
    
    # Workouts in this program
    workouts = db.relationship("WorkoutModel", back_populates="program", cascade="all, delete")

    @staticmethod
    def has_owner(self):
        return True
        
    # Returns True is the given user id is considered the owner of this tracker entry
    def check_owner(self, id):
        return self.owner_id == id
        
    def __str__(self):
        return "%u ProgramModel: %s, %u(%s), public(%s)" % (self.id, self.name, self.owner_id, self.owner.username, str(self.is_public))
