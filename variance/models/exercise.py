"""
Module containing models for exercises.
"""
from variance.extensions import db, ResourceBase


"Table that associates EquipmentModel and ExerciseModel. Allows for the Many-to-Many relationship between exercises and equipment. ie. Allows for equipment to be used by many differe exercises, and exercises to use many differen pieces of equipment"
ExerciseEquipmentAssociationTable = db.Table(
    "ExerciseEquipmentAssociation",
    db.metadata,
    db.Column("equipment_uuid", db.ForeignKey("EquipmentIndex.uuid")),
    db.Column("exercise_uuid", db.ForeignKey("ExerciseIndex.uuid"))
)

"""
This association table maps exercises to the collection of muscles
that the exercise targets. The "intensity" column is a relative measure
of how much a muscle is worked by the exercise that should vary from 0 to 1
"""
ExerciseMuscleAssociation= db.Table(
    "ExerciseMuscleAssociation",
    db.metadata,
    db.Column("exercise_uuid", db.ForeignKey("ExerciseIndex.uuid")),
    db.Column("muscle_uuid", db.ForeignKey("MuscleIndex.uuid")),
    db.Column("intensity", db.Float(), nullable=False)
)

class ExerciseModel(ResourceBase):
    "Model for representing exercises that users can perform"
    __tablename__ = "ExerciseIndex"

    name = db.Column(db.String(100), nullable=False)
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

    parent_exercise_uuid = db.Column(
        db.String(36), db.ForeignKey("ExerciseIndex.uuid"), 
        nullable=True)
    "Is this exercise a variation of another exercise, if so, which exercise?    (Ex: Close grip bench is a variation of bench press)"
    parent_exercise = db.relationship(
        "ExerciseModel",
        foreign_keys="ExerciseModel.parent_exercise_uuid",
        back_populates="variations")
    
    variations = db.relationship("ExerciseModel")

    def __str__(self) -> str:
        return "%s - Exercise: %s dur(%s), dis(%s), wght(%s)" % (self.uuid, self.name, str(self.use_duration), str(self.use_distance), str(self.use_weight))
