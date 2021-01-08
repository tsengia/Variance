from variance import db

# Association table. Associates MuscleGroups with their Muscles and vice-versa
class MuscleGroupAssociationTable(db.Table):
    __tablename__ = "MuscleGroupAssociation"
    group_id = db.Column(db.Integer, db.ForeignKey("MuscleGroupIndex.id"))
    muscle_id = db.Column(db.Integer, db.ForeignKey("MuscleIndex.id"))

class MuscleGroupModel(db.Model):
    __tablename__ = "MuscleGroupIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of this muscle group
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # List of muscles in this muscle group
    muscles = db.relationship("MuscleModel", secondary="MuscleGroupAssociation", back_populates="groups")

class MuscleModel(db.Model):
    __tablename__ = "MuscleIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Optional: ID of this muscle used to locate on the anatomy chart
    diagram_id = db.Column(db.Integer, nullable=True)

    # Long, anatomical name for this muscle
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Shortened name for this muscle. Used for display.
    short_name = db.Column(db.String(50), nullable=True)

    # List of groups this muscle belongs to
    groups = db.relationship("MuscleGroupModel", secondary="MuscleGroupAssociation", back_populates="muscles")
    
    # List of exercises that this muscle is used in as a primary muscle
    primary_exercises = db.relationship("MuscleGroupModel", secondary="PrimaryExerciseMuscleAssociation", back_populates="primary_muscles")
    
    # List of exercises that this muscle is used in as a secondary muscle
    secondary_exercises = db.relationship("MuscleGroupModel", secondary="SecondaryExerciseMuscleAssociation", back_populates="secondary_muscles")