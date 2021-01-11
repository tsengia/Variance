from variance import db 

class ExerciseModel(db.Model):
    __tablename__ = "ExerciseIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the exercise
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # What type of movement is this? Push? Pull? Hinge? etc.
    movement = db.Column(db.String(30), nullable=True)

    # Is this exercise measured in time?
    use_duration = db.Column(db.Boolean, nullable=False, default=0)

    # Is this exercise measured in distance?
    use_distance = db.Column(db.Boolean, nullable=False, default=0)

    # Is this exercise measured in weight?
    use_weight = db.Column(db.Boolean, nullable=False, default=0)

    # List of primary muscles worked by this exercise
    primary_muscles = db.relationship("MuscleModel", secondary="PrimaryExerciseMuscleAssociation", back_populates="primary_exercises")

    # List of secondary muscles worked by this exercise
    secondary_muscles = db.relationship("MuscleModel", secondary="SecondaryExerciseMuscleAssociation", back_populates="secondary_exercises")