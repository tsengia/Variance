from variance.extensions import db


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
    # Example: The "length" dimension's base unit is centimeters, there are
    # 100cm in 1m, so for the meters unit this would be set to 100
    multiplier = db.Column(db.Float(decimal_return_scale=4),
                           nullable=False, default=1.0)

    # Can this unit be deleted? (Basically, is this a user defined unit or a pre-packaged unit?)
    # Example: Because the meters unit comes as a default unit in Variance,
    # this would be set to False.
    removable = db.Column(db.Boolean, default=True)

    @staticmethod
    def has_owner():
        return False

    @staticmethod
    def get_id_by_name(text):
        name_match = UnitModel.query.filter_by(name=text).first()
        if name_match:
            return name_match.id

    @staticmethod
    def get_id_by_abbreviation(text):
        abbreviation_match = UnitModel.query.filter_by(
            abbreviation=text).first()
        if abbreviation_match:
            return abbreviation_match.id

    def __str__(self):
        return "UnitModel (%i): %s (%s) %s, removable(%s), mult(%s) " % (int(
            self.id), self.name, self.abbreviation, self.dimension, str(self.removable), str(self.multiplier))

    def __int__(self):
        return int(self.multiplier)

    def __float__(self):
        return float(self.multiplier)
