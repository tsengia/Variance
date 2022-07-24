"""
Module containing the EquipmentModel
"""
from variance.extensions import db, ResourceBase
import uuid

class EquipmentModel(ResourceBase):
    """
    Model for a piece of exercise equipment.
    Examples: Dumbbells, Barbell, Treadmill, Bench.

    Instances are stored in the `EquipmentIndex` table.
    """

    __tablename__ = "EquipmentIndex"

    name = db.Column(db.String(40), nullable=False)
    " Name of this piece of equipment. Example: 'Dumbbells'"

    description = db.Column(db.String(200), nullable=True)
    " Describe this piece of equipment."

    exercises = db.relationship(
        "ExerciseModel", 
        secondary="ExerciseEquipmentAssociation",
        back_populates="equipment")
    " List of exercises that use this piece of equipment. "

    def __str__(self):
        return "{0}: {1}".format(self.uuid, self.name)
