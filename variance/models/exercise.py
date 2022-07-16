"""
Module containing models for exercises.
"""
from variance.extensions import db


class ExerciseEquipmentAssociation(db.Model):
    "Model that associates EquipmentModel and ExerciseModel. Allows for the Many-to-Many relationship between exercises and equipment. ie. Allows for equipment to be used by many differe exercises, and exercises to use many differen pieces of equipment"
    __tablename__ = "ExerciseEquipmentList"

    equipment_id = db.Column(db.Integer, db.ForeignKey(
        "EquipmentIndex.id"), nullable=False, primary_key=True)

    exercise_id = db.Column(db.Integer, 
        db.ForeignKey("ExerciseIndex.id"), nullable=False, primary_key=True)

    def __str__(self):
        return "GymEquipAssoc: %u  -> %u " % (self.exercise.id, self.equipment.id)


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
        secondary="ExerciseEquipmentList", back_populates="exercises")
    "Pieces of equipment does this exercise uses."

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
