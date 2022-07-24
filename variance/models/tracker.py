"""
Module containing models used for user-created trackers.
"""

from datetime import datetime
from variance.extensions import db, ResourceBase


class TrackerModel(ResourceBase):
    "Representation of a user-created tracker. For example, tracking hours of sleep."
    __tablename__ = "TrackerIndex"
    name = db.Column(db.String(40), nullable=False)
    "Display name of this tracker."
    dimension = db.Column(db.String(20), nullable=False)
    "The base dimension/unit that this tracker tracks. For example, the sleep tracker would have a dimension of 'duration'"

    entries = db.relationship("TrackerEntryModel", back_populates="tracker")
    "List of entries this user has entered into this tracker"

    def __str__(self) -> str:
        return "%s Tracker: %s (%s), user %s (%u)" % (int(self.uuid),\
            str(self.name), str(self.dimension),\
            str(self.owner.username), int(self.owner_uuid))


class TrackerEntryModel(ResourceBase):
    "Representation of an entry into a user-created TrackerModel"
    __tablename__ = "TrackerEntries"
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    "Timestamp of when this entry was made."
    value = db.Column(db.Float, nullable=False)
    "Value entered in this tracker entry."

    unit_uuid = db.Column(db.String(36), db.ForeignKey(
        "UnitIndex.uuid"), nullable=False)
    unit = db.relationship("UnitModel",\
        foreign_keys="TrackerEntryModel.unit_uuid")
    "UnitModel that his entry is using for its value"

    parent_tracker_uuid = db.Column(
        db.String(36), db.ForeignKey("TrackerIndex.uuid"), nullable=False)
    "ID of the TrackerModel that this entry is in"
    tracker = db.relationship("TrackerModel",\
        back_populates="entries",\
        foreign_keys="TrackerEntryModel.parent_tracker_uuid")
    "TrackerModel that this entry is in"

    def __str__(self) -> str:
        return "%s Tracker Entry: %s %s, tracker (%s) @ %s" % \
            (int(self.uuid), str(self.value), str(self.unit.abbreviation),\
            int(self.parent_tracker_uuid), str(self.time))
