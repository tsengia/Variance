"""
Module containing models for exercises.
"""
from variance.extensions import db


"Table that associates EquipmentModel and ExerciseModel. Allows for the Many-to-Many relationship between exercises and equipment. ie. Allows for equipment to be used by many differe exercises, and exercises to use many differen pieces of equipment"
ExerciseEquipmentAssociationTable = db.Table(
    "ExerciseEquipmentAssociation",
    db.metadata,
    db.Column("equipment_id", db.ForeignKey("EquipmentIndex.id")),
    db.Column("exercise_id", db.ForeignKey("ExerciseIndex.id"))
)

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

class ExerciseModel(db.Model):
    "Model for representing exercises that users can perform"
    __tablename__ = "ExerciseIndex"

    id = db.Column(db.Integer, primary_key=True)
    "Unique primary key for database."
    
    canonical_name = db.Column(db.String(100), unique=True, nullable=False)
    "Internal name of the exercise for linking, import, and export"

    name = db.Column(db.String(100), unique=True, nullable=False)
    "Name of the exercise to display to the user."
    
    description = db.Column(db.Text, nullable=True)
    "Description of this exercise."

    use_duration = db.Column(db.Boolean, nullable=False, default=0)
    "Set to True if this exercises is measured in time."

    use_distance = db.Column(db.Boolean, nullable=False, default=0)
    "Set to True if this exercise is measured in distance."

    use_weight = db.Column(db.Boolean, nullable=False, default=0)
    "Set to True if this exercise is measured in weight."

    equipment = db.relationship(
        "EquipmentModel", 
        secondary="ExerciseEquipmentAssociation", 
        back_populates="exercises")
    "Pieces of equipment does this exercise uses."

    muscles = db.relationship(
        "MuscleModel",
        secondary="ExerciseMuscleAssociation",
        back_populates="exercises")
    "Muscles that this exercise activates.."

    parent_exercise_id = db.Column(
        db.Integer, db.ForeignKey("ExerciseIndex.id"), nullable=True)
    "Is this exercise a variation of another exercise, if so, which exercise?    (Ex: Close grip bench is a variation of bench press)"
    parent_exercise = db.relationship(
        "ExerciseModel",
        foreign_keys="ExerciseModel.parent_exercise_id",
        back_populates="variations")
    
    variations = db.relationship("ExerciseModel")

    def __str__(self) -> str:
        return "%u - %s Exercise: %s dur(%s), dis(%s), wght(%s)" % (self.id, self.canonical_name, self.name, str(self.use_duration), str(self.use_distance), str(self.use_weight))

    @staticmethod
    def has_owner() -> bool:
        return False
