from variance import db 

class GymEquipmentModel(db.Model):
    __tablename__ = "GymEquipmentList"
    
    equipment_id = db.Column(db.Integer, db.ForeignKey("EquipmentIndex.id"), nullable=False)
    equipment = db.relationship("EquipmentModel", foreign_keys="GymEquipmentModel.equipment_id")
    
    gym_id = db.Column(db.Integer, db.ForeignKey("GymIndex.id"), nullable=False)
    gym = db.relationship("GymModel", foreign_keys="GymEquipmentModel.gym_id")

class GymModel(db.Model):
    __tablename__ = "GymIndex"

    ###
    # Every Gym can have multiple pieces of equipment associated with it.
    # Gyms can be public or private (private by default).
    # Gyms are really nothing more than a collection of equipment, making it easier to plan workouts
    #
    ###

    id = db.Column(db.Integer, primary_key=True)

    # Name of the gym
    name = db.Column(db.String(100), unique=False, nullable=False)
    
    # Location of the gym
    location = db.Column(db.String(100), nullable=True)
    
    description = db.Column(db.Text, nullable=True)

    ### Ownership and visibility
    # Is this gym visible to all users? If set to true, then all users can use this gym
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    
    # The user who added this gym to the database
    created_by_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    created_by = db.relationship("UserModel", back_populates="recipies")
    