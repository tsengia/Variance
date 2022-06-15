from variance.extensions import db


class EquipmentModel(db.Model):
    """
    Model for a piece of exercise equipment.
    Examples: Dumbbells, Barbell, Treadmill, Bench.

    Instances are stored in the `EquipmentIndex` table.

    Attributes:
        id - Unique integer ID, primary key
        canonical_name - Unique string used during import, export, and linking
        name - Non-unique display string for users to see
        description - String explaining what this piece of equipment is
        exercises - List of ExerciseModels that use this piece of equipment
    """

    __tablename__ = "EquipmentIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of this piece of equipment. Example: "example-equipment"
    canonical_name = db.Column(db.String(40), unique=True, nullable=False)

    # Name of this piece of equipment. Example: "Dumbbells"
    name = db.Column(db.String(40), unique=True, nullable=False)

    # Describe this piece of equipment.
    description = db.Column(db.String(20), nullable=True)

    # List of exercises that use this piece of equipment.
    exercises = db.relationship(
        "ExerciseModel", 
        secondary="ExerciseEquipmentList",
        back_populates="equipment")
