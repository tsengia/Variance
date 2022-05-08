from variance.extensions import db


class EquipmentModel(db.Model):
    __tablename__ = "EquipmentIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of this piece of equipment. Example: "Dumbbells"
    name = db.Column(db.String(40), unique=True, nullable=False)

    # Describe this piece of equipment.
    description = db.Column(db.String(20), nullable=True)

    # List of exercises that use this piece of equipment.
    exercises = db.relationship(
        "ExerciseModel", 
        secondary="ExerciseEquipmentList",
        back_populates="equipment")
