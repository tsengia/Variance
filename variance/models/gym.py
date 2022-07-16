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

    ### Ownership and visibility
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    "Is this gym visible to all users? If set to true, then all users can use this gym"

    owner_id = db.Column(db.Integer, db.ForeignKey(
        "UserIndex.id"), nullable=False)
    " The user id who added this gym to the database "
    owner = db.relationship("UserModel", backref="gyms")

    equipment = db.relationship("EquipmentModel", secondary="GymEquipmentList")
    "Many to many relationship that represents all types of equipment that can be found in this gym"

    @staticmethod
    def has_owner() -> bool:
        "Static helper function for the authorization algorithm to know that this type of resource does have a well-defined owner and should check ownership before performing actions."
        return True

    def check_owner(self, id: int) -> bool:
        "Returns true if the owner_id is equal to the provided ID"
        return self.owner.id == id

    def __str__(self) -> str:
        return "%u Gym: %s public(%s), owned by %u (%s)" % (
            self.id, self.name, str(self.is_public), self.owner.id, self.owner.username)
