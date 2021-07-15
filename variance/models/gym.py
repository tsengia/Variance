from variance.extensions import db


class GymEquipmentAssociation(db.Model):
    __tablename__ = "GymEquipmentList"

    equipment_id = db.Column(db.Integer, db.ForeignKey(
        "EquipmentIndex.id"), nullable=False, primary_key=True)
    equipment = db.relationship(
        "EquipmentModel", foreign_keys="GymEquipmentAssociation.equipment_id")

    gym_id = db.Column(db.Integer, db.ForeignKey(
        "GymIndex.id"), nullable=False, primary_key=True)
    gym = db.relationship(
        "GymModel", foreign_keys="GymEquipmentAssociation.gym_id")

    def __str__(self):
        return "GymEquipAssoc: %u (%s) -> %u (%s)" % (self.gym.id,
                                                      self.gym.name, self.equipment.id, self.equipment.name)


class GymModel(db.Model):
    __tablename__ = "GymIndex"

    """
    Every Gym can have multiple pieces of equipment associated with it.
    Gyms can be public or private (private by default).
    Gyms are really nothing more than a collection of equipment, making it easier to plan workouts
    """

    id = db.Column(db.Integer, primary_key=True)

    # Name of the gym
    name = db.Column(db.String(100), unique=False, nullable=False)

    # Location of the gym
    location = db.Column(db.String(100), nullable=True)

    description = db.Column(db.Text, nullable=True)

    ### Ownership and visibility
    # Is this gym visible to all users? If set to true, then all users can use
    # this gym
    is_public = db.Column(db.Boolean, nullable=False, default=False)

    # The user who added this gym to the database
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", backref="gyms")

    equipment = db.relationship("EquipmentModel", secondary="GymEquipmentList")

    @staticmethod
    def has_owner():
        return True

    def check_owner(self, id):
        return self.owner.id == id

    def __str__(self):
        return "%u Gym: %s public(%s), owned by %u (%s)" % (
            self.id, self.name, str(self.is_public), self.owner.id, self.owner.username)
