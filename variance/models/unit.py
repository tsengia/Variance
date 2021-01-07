from variance import db

class UnitModel(db.Model):
    __tablename__ = "UnitIndex"

    id = db.Column(db.Integer, primary_key=True)
    # Long name, plural form of this unit. Example: "meters"
    name = db.Column(db.String(40), unique=True, nullable=False)

    # Short form of this unit. Example: "m"
    abbreviation = db.Column(db.String(20), nullable=False)

    # What does this unit measure? Example: "length"
    dimension = db.Column(db.String(20), nullable=False)

    # What do we multiply this unit by to get the base unit for the dimension?
    # Example: The "length" dimension's base unit is centimeters, there are 100cm in 1m, so for the meters unit this would be set to 100
    multiplier = db.Column(db.Float(decimal_return_scale=4), nullable=False, default=1.0)

    # Can this unit be deleted? (Basically, is this a user defined unit or a pre-packaged unit?)
    # Example: Because the meters unit comes as a default unit in Variance, this would be set to False.
    removable = db.Column(db.Boolean, default=True)