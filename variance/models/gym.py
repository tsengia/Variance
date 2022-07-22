"""
Modules that contains the GymModel and the GymEquipmentAssociation table
"""
from variance.extensions import db


"Association table that provides the Many to Many relationship between Equipment and Gyms."
GymEquipmentAssociation = db.Table(
    "GymEquipmentList",
    db.metadata,
    db.Column("equipment_id", db.ForeignKey("EquipmentIndex.id")),
    db.Column("gym_id", db.ForeignKey("GymIndex.id"))
)

class GymModel(db.Model):
    """
    Every Gym can have multiple pieces of equipment associated with it.
    Gyms can be public or private (private by default).
    Gyms are really nothing more than a collection of equipment, making it easier to plan workouts
    """
    __tablename__ = "GymIndex"


    id = db.Column(db.Integer, primary_key=True)
    "Unique ID for the GymModel instance, used as primary key in DB."

    name = db.Column(db.String(100), unique=False, nullable=False)
    "Name of the gym"

    location = db.Column(db.String(100), nullable=True)
    "Location of the gym"

    description = db.Column(db.Text, nullable=True)
    "Description of the gym"

    equipment = db.relationship("EquipmentModel", secondary="GymEquipmentList")
    "Many to many relationship that represents all types of equipment that can be found in this gym"

    def __str__(self) -> str:
        return "%u Gym: %s public(%s), owned by %u (%s)" % (
            self.id, self.name, str(self.is_public), self.owner.id, self.owner.username)
