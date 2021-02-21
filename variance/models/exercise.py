from datetime import datetime

from variance import db 

# This is for dynamically calculated measures.
# For example: 90% of 1 rep max, or 1/2 the pace of the PR time, etc.
class LambdaModel(db.Model):
    __tablename__ = "LambdaIndex"
    
    id = db.Column(db.Integer, primary_key=True)

    # Name of this lambda function, for example: "Percentage of 1 Rep Max"
    name = db.Column(db.String(100), nullable=False)
    
    # Callable/internal name of this lambda function, for example "percent_1rm"
    function_name = db.Column(db.String(40), nullable=False)

# These are sets that have been completed by users
class SetEntryModel(db.Model):
    __tablename__ = "SetEntryIndex"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Time this set was done/entered
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
    owner_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", foreign_keys="SetEntryModel.owner_id", back_populates="set_entries")
    
    @staticmethod
    def has_owner(self):
        return True
        
    # Returns True is the given user id is considered the owner of this set entry
    def check_owner(self, id):
        return self.owner_id == id

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

# Theses are sets that are planned to be completed (in a workout plan)
class SetPlanModel(db.Model):
    __tablename__ = "SetPlanIndex"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # What exercise is being done for this set?
    exercise_id = db.Column(db.Integer, db.ForeignKey("ExerciseIndex.id"), nullable=False)
    exercise = db.relationship("ExerciseModel", foreign_keys="SetPlanModel.exercise_id")
    
    # What workout day does this belond to?
    workout_id = db.Column(db.Integer, db.ForeignKey("WorkoutDayIndex.id"), nullable=False)
    workout = db.relationship("WorkoutDayModel", foreign_keys="SetPlanModel.workout_id", back_populates="sets")
    
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
    duration_lambda_id = db.Column(db.Integer, db.ForeignKey("LambdaIndex.id"), nullable=True)
    duration_lambda = db.relationship("LambdaModel", foreign_keys="SetPlanModel.duration_lambda_id")
    
    distance_lambda_id = db.Column(db.Integer, db.ForeignKey("LambdaIndex.id"), nullable=True)
    distance_lambda = db.relationship("LambdaModel", foreign_keys="SetPlanModel.distance_lambda_id")
    
    weight_lambda_id = db.Column(db.Integer, db.ForeignKey("LambdaIndex.id"), nullable=True)
    weight_lambda = db.relationship("LambdaModel", foreign_keys="SetPlanModel.weight_lambda_id")
    
    # Parameters to be passed in to the lambda function. Examples are: percentage, days, ratios, another exercise
    lambda_param1 = db.Column(db.Float, nullable=True)
    lambda_param2 = db.Column(db.Float, nullable=True)
    lambda_param3 = db.Column(db.Float, nullable=True)
    lambda_exercise_param1_id = db.Column(db.Integer, db.ForeignKey("ExerciseIndex.id"), nullable=True)
    lambda_exercise_param1 = db.relationship("ExerciseModel", foreign_keys="SetPlanModel.lambda_exercise_param1_id")

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

class WorkoutDayModel(db.Model):
    __tablename__ = "WorkoutDayIndex"
    
    id = db.Column(db.Integer, primary_key=True)

    # Name of the workout day
    name = db.Column(db.String(100), nullable=False)
    
    # What day does this occur on? Freeform entry
    day = db.Column(db.String(20), nullable=True)
    
    # Sets of exercises that are performed on this day
    sets = db.relationship("SetPlanModel", back_populates="workout", cascade="all, delete")

    # What workout week does this belond to?
    week_id = db.Column(db.Integer, db.ForeignKey("WorkoutWeekIndex.id"), nullable=False)
    week = db.relationship("WorkoutWeekModel", foreign_keys="WorkoutDayModel.week_id", back_populates="days")

    @staticmethod
    def has_owner(self):
        return True
        
    # Returns True is the given user id is considered the owner of this tracker entry
    def check_owner(self, id):
        return self.week.check_owner(id)

class WorkoutWeekModel(db.Model):
    __tablename__ = "WorkoutWeekIndex"
    
    id = db.Column(db.Integer, primary_key=True)

    # Name of the workout day
    name = db.Column(db.String(100), nullable=False)
    
    # WorkoutDays in this week
    days = db.relationship("WorkoutDayModel", back_populates="week", cascade="all, delete")

    # What day does this occur on? Freeform entry
    day = db.Column(db.String(20), nullable=True)
    
    # What workout program does this belond to?
    program_id = db.Column(db.Integer, db.ForeignKey("WorkoutProgramIndex.id"), nullable=False)
    program = db.relationship("WorkoutProgramModel", foreign_keys="WorkoutWeekModel.program_id", back_populates="weeks")


    @staticmethod
    def has_owner(self):
        return True
        
    # Returns True is the given user id is considered the owner of this tracker entry
    def check_owner(self, id):
        return self.program.check_owner(id)

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
    
    # WorkoutWeeks in this program
    weeks = db.relationship("WorkoutWeekModel", back_populates="program", cascade="all, delete")

    @staticmethod
    def has_owner(self):
        return True
        
    # Returns True is the given user id is considered the owner of this tracker entry
    def check_owner(self, id):
        return self.owner_id == id

class ExerciseModel(db.Model):
    __tablename__ = "ExerciseIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the exercise
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # What type of movement is this? Push? Pull? Hinge? etc.
    movement = db.Column(db.String(30), nullable=True)
    
    # What type of joint action is this? Flexion? Extension? Abduction? Adduction? Rotation? Circumduction?
    joint_action = db.Column(db.String(30), nullable=True)

    # Is this exercise measured in time?
    use_duration = db.Column(db.Boolean, nullable=False, default=0)

    # Is this exercise measured in distance?
    use_distance = db.Column(db.Boolean, nullable=False, default=0)

    # Is this exercise measured in weight?
    use_weight = db.Column(db.Boolean, nullable=False, default=0)
    
    # What piece of equipment does this exercise use?
    equipment_id = db.Column(db.Integer, db.ForeignKey("EquipmentIndex.id"), nullable=True)
    equipment = db.relationship("EquipmentModel")

    # Is this exercise a variation of another exercise, if so, which exercise? (Ex: Close grip bench is a variation of bench press)
    parent_exercise_id = db.Column(db.Integer, db.ForeignKey("ExerciseIndex.id"), nullable=True)
    parent_exercise = db.relationship("ExerciseModel", foreign_keys="ExerciseModel.parent_exercise_id", back_populates="variations")
    variations = db.relationship("ExerciseModel")
    
    # List of primary muscles worked by this exercise
    primary_muscles = db.relationship("MuscleModel", secondary="PrimaryExerciseMuscleAssociation", back_populates="primary_exercises")

    # List of secondary muscles worked by this exercise
    secondary_muscles = db.relationship("MuscleModel", secondary="SecondaryExerciseMuscleAssociation", back_populates="secondary_exercises")
    
    @staticmethod
    def has_owner():
        return False