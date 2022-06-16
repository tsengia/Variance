"""
Module containing the EquipmentModel
"""
from variance.extensions import db


class EquipmentModel(db.Model):
    """
    Model for a piece of exercise equipment.
    Examples: Dumbbells, Barbell, Treadmill, Bench.

    Instances are stored in the `EquipmentIndex` table.
    """

    __tablename__ = "EquipmentIndex"

    id = db.Column(db.Integer, primary_key=True)
    " Unique ID for the EquipmentModel instance, is the primary key."

    canonical_name = db.Column(db.String(40), unique=True, nullable=False)
    " Name of this piece of equipment. Example: 'example-equipment' "

    name = db.Column(db.String(40), unique=True, nullable=False)
    " Name of this piece of equipment. Example: 'Dumbbells'"

    description = db.Column(db.String(200), nullable=True)
    " Describe this piece of equipment."

    exercises = db.relationship(
        "ExerciseModel", 
        secondary="ExerciseEquipmentList",
        back_populates="equipment")
    " List of exercises that use this piece of equipment. "
