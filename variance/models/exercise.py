from variance import db 

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