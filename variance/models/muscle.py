from variance import db

# Association table. Associates MuscleGroups with their Muscles and vice-versa


class MuscleGroupAssociationTable(db.Model):
    __tablename__ = "MuscleGroupAssociation"
    group_id = db.Column(db.Integer, db.ForeignKey(
        "MuscleGroupIndex.id"), primary_key=True)
    muscle_id = db.Column(db.Integer, db.ForeignKey(
        "MuscleIndex.id"), primary_key=True)

    def __str__(self):
        return "MuscleGroupAssociation: group %u -> muscle %u" % (
            self.group_id, self.muscle_id)


class MuscleGroupModel(db.Model):
    __tablename__ = "MuscleGroupIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of this muscle group
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # List of muscles in this muscle group
    muscles = db.relationship(
        "MuscleModel",
        secondary="MuscleGroupAssociation",
        back_populates="groups")

    @staticmethod
    def has_owner():
        return False

    def __str__(self):
        return "%u MuscleGroupModel: %s" % (self.id, self.name)


class MuscleModel(db.Model):
    __tablename__ = "MuscleIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Optional: ID of this muscle used to locate on the anatomy chart
    diagram_id = db.Column(db.Integer, nullable=True)

    # Long, anatomical name for this muscle
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Shortened name for this muscle. Used for display.
    short_name = db.Column(db.String(50), nullable=True)

    # List of groups this muscle belongs to
    groups = db.relationship(
        "MuscleGroupModel",
        secondary="MuscleGroupAssociation",
        back_populates="muscles")

    @staticmethod
    def has_owner():
        return False

    def __str__(self):
        return "%i MuscleModel: %s" % (self.id, self.name)


class MuscleSectionModel(db.Model):
    __tablename__ = "MuscleSectionIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Optional: ID of this muscle section sused to locate on the anatomy chart
    diagram_id = db.Column(db.Integer, nullable=True)

    # Name of this muscle section. For example "Upper pec"
    name = db.Column(db.String(100), unique=True, nullable=False)

    # What muscle is this muscle section of?
    parent_muscle_id = db.Column(
        db.Integer, db.ForeignKey("MuscleIndex.id"), nullable=False)
    parent_muscle = db.relationship("MuscleModel", backref="sections")

    @staticmethod
    def has_owner():
        return False

    def __str__(self):
        return "%i MuscleSectionModel: %s" % (self.id, self.name)
