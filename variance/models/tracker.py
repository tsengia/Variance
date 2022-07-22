"""
Module containing models used for user-created trackers.
"""

from datetime import datetime
from variance.extensions import db


class TrackerModel(db.Model):
    "Representation of a user-created tracker. For example, tracking hours of sleep."
    __tablename__ = "TrackerIndex"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    "Display name of this tracker."
    dimension = db.Column(db.String(20), nullable=False)
    "The base dimension/unit that this tracker tracks. For example, the sleep tracker would have a dimension of 'duration'"

    entries = db.relationship("TrackerEntryModel", back_populates="tracker")
    "List of entries this user has entered into this tracker"

    def __str__(self) -> str:
        return "%u Tracker: %s (%s), user %s (%u)" % (int(self.id),\
            str(self.name), str(self.dimension),\
            str(self.owner.username), int(self.owner_id))


class TrackerEntryModel(db.Model):
    "Representation of an entry into a user-created TrackerModel"
    __tablename__ = "TrackerEntries"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    "Timestamp of when this entry was made."
    value = db.Column(db.Float, nullable=False)
    "Value entered in this tracker entry."

    unit_id = db.Column(db.Integer, db.ForeignKey(
        "UnitIndex.id"), nullable=False)
    unit = db.relationship("UnitModel",\
        foreign_keys="TrackerEntryModel.unit_id")
    "UnitModel that his entry is using for its value"

    parent_tracker_id = db.Column(
        db.Integer, db.ForeignKey("TrackerIndex.id"), nullable=False)
    "ID of the TrackerModel that this entry is in"
    tracker = db.relationship("TrackerModel",\
        back_populates="entries",\
        foreign_keys="TrackerEntryModel.parent_tracker_id")
    "TrackerModel that this entry is in"

    def __str__(self) -> str:
        return "%u Tracker Entry: %s %s, tracker (%u) @ %s" % \
            (int(self.id), str(self.value), str(self.unit.abbreviation),\
            int(self.parent_tracker_id), str(self.time))
