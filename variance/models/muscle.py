"Modules containing models and associations for Musles and MuscleGroups"

from variance.extensions import db

"Association table. Associates MuscleGroups with their Muscles and vice-versa"
MuscleGroupAssociationTable = db.Table(
    "MuscleGroupAssociation",
    db.metadata,
    db.Column("group_id", db.ForeignKey(
        "MuscleGroupIndex.id")),
    db.Column("muscle_id", db.ForeignKey(
        "MuscleIndex.id"))
)

class MuscleGroupModel(db.Model):
    "Representation of a named group of muscles. Ex: Legs"
    __tablename__ = "MuscleGroupIndex"

    id = db.Column(db.Integer, primary_key=True)
    
    canonical_name = db.Column(db.String(100), unique=True, nullable=False)
    "Canonical name used when exporting and importing/linking data."

    name = db.Column(db.String(100), unique=True, nullable=False)
    "Display name of this muscle group"
    
    description = db.Column(db.Text, nullable=True)

    muscles = db.relationship(
        "MuscleModel",
        secondary=MuscleGroupAssociationTable,
        back_populates="groups")
    "List of muscles in this muscle group"

    @staticmethod
    def has_owner() -> bool:
        return False

    def __str__(self) -> str:
        return "%u MuscleGroupModel: %s" % (self.id, self.name)


class MuscleModel(db.Model):
    "Representation of a muscle."
    __tablename__ = "MuscleIndex"

    id = db.Column(db.Integer, primary_key=True)

    diagram_id = db.Column(db.Integer, nullable=True)
    "Optional: ID of this muscle used to locate on the anatomy chart"

    canonical_name = db.Column(db.String(100), unique=True, nullable=False)
    "Canonical name used when exporting and importing/linking data."
    
    name = db.Column(db.String(100), unique=True, nullable=False)
    "Long, anatomical name for this muscle"

    short_name = db.Column(db.String(50), nullable=True)
    "Shortened name for this muscle. Used for display."

    groups = db.relationship(
        "MuscleGroupModel",
        secondary=MuscleGroupAssociationTable,
        back_populates="muscles")
    "List of Muscle Groups this muscle belongs to."

    exercises = db.relationship(
        "ExerciseModel",
        secondary="ExerciseMuscleAssociation",
        back_populates="muscles")
    "List of exercises that activate this muscle."

    @staticmethod
    def has_owner() -> bool:
        return False

    def __str__(self) -> str:
        return "%i MuscleModel: %s" % (self.id, self.name)


class MuscleSectionModel(db.Model):
    "Representation of a section of Muscle."
    __tablename__ = "MuscleSectionIndex"

    id = db.Column(db.Integer, primary_key=True)

    diagram_id = db.Column(db.Integer, nullable=True)
    "Optional: ID of this muscle section sused to locate on the anatomy chart"

    name = db.Column(db.String(100), unique=True, nullable=False)
    "Name of this muscle section. For example 'Upper pec'"

    parent_muscle_id = db.Column(
        db.Integer, db.ForeignKey("MuscleIndex.id"), nullable=False)
    "The larger muscle that this section is a part of."
    parent_muscle = db.relationship("MuscleModel", backref="sections")

    @staticmethod
    def has_owner() -> bool:
        return False

    def __str__(self) -> str:
        return "%i MuscleSectionModel: %s" % (self.id, self.name)
