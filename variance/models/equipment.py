from variance import db

class Equipment(db.Model):
    __tablename__ = "EquipmentIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of this piece of equipment. Example: "Dumbbells"
    name = db.Column(db.String(40), unique=True, nullable=False)

    # Describe this piece of equipment.
    description = db.Column(db.String(20), nullable=True)