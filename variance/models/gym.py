"""
Modules that contains the GymModel and the GymEquipmentAssociation table
"""
from variance.extensions import db, ResourceBase


"Association table that provides the Many to Many relationship between Equipment and Gyms."
GymEquipmentAssociation = db.Table(
    "GymEquipmentList",
    db.metadata,
    db.Column("equipment_uuid", db.ForeignKey("EquipmentIndex.uuid")),
    db.Column("gym_uuid", db.ForeignKey("GymIndex.uuid"))
)

class GymModel(ResourceBase):
    """
    Every Gym can have multiple pieces of equipment associated with it.
    Gyms can be public or private (private by default).
    Gyms are really nothing more than a collection of equipment, making it easier to plan workouts
    """
    __tablename__ = "GymIndex"

    name = db.Column(db.String(100), unique=False, nullable=False)
    "Name of the gym"

    location = db.Column(db.String(100), nullable=True)
    "Location of the gym"

    description = db.Column(db.Text, nullable=True)
    "Description of the gym"

    equipment = db.relationship("EquipmentModel", secondary="GymEquipmentList")
    "Many to many relationship that represents all types of equipment that can be found in this gym"

    def __str__(self) -> str:
        return "%s Gym: %s public(%s), owned by %u (%s)" % (
            self.uuid, self.name, str(self.is_public), self.owner.uuid, self.owner.username)
