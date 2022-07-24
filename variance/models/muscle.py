"Modules containing models and associations for Musles and MuscleGroups"

from variance.extensions import db, ResourceBase

"Association table. Associates MuscleGroups with their Muscles and vice-versa"
MuscleGroupAssociationTable = db.Table(
    "MuscleGroupAssociation",
    db.metadata,
    db.Column("group_uuid", db.ForeignKey(
        "MuscleGroupIndex.uuid")),
    db.Column("muscle_uuid", db.ForeignKey(
        "MuscleIndex.uuid"))
)

class MuscleGroupModel(ResourceBase):
    "Representation of a named group of muscles. Ex: Legs"
    __tablename__ = "MuscleGroupIndex"

    name = db.Column(db.String(100), nullable=False)
    "Display name of this muscle group"
    
    description = db.Column(db.Text, nullable=True)

    muscles = db.relationship(
        "MuscleModel",
        secondary=MuscleGroupAssociationTable,
        back_populates="groups")
    "List of muscles in this muscle group"

    def __str__(self) -> str:
        return "%s MuscleGroupModel: %s" % (self.uuid, self.name)


class MuscleModel(ResourceBase):
    "Representation of a muscle."
    __tablename__ = "MuscleIndex"

    diagram_id = db.Column(db.Integer, nullable=True)
    "Optional: ID of this muscle used to locate on the anatomy chart"

    name = db.Column(db.String(100), nullable=False)
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

    def __str__(self) -> str:
        return "%s MuscleModel: %s" % (self.uuid, self.name)


class MuscleSectionModel(ResourceBase):
    "Representation of a section of Muscle."
    __tablename__ = "MuscleSectionIndex"

    diagram_id = db.Column(db.Integer, nullable=True)
    "Optional: ID of this muscle section used to locate on the anatomy chart"

    name = db.Column(db.String(100), nullable=False)
    "Name of this muscle section. For example 'Upper pec'"

    parent_muscle_uuid = db.Column(
        db.String(36), db.ForeignKey("MuscleIndex.uuid"), nullable=False)
    "The larger muscle that this section is a part of."
    parent_muscle = db.relationship("MuscleModel", backref="sections")

    def __str__(self) -> str:
        return "%s MuscleSectionModel: %s" % (self.uuid, self.name)
