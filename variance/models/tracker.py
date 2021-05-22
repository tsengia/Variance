from datetime import datetime
from variance import db


class TrackerModel(db.Model):
    __tablename__ = "TrackerIndex"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    dimension = db.Column(db.String(20), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey(
        "UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", back_populates="trackers")

    entries = db.relationship("TrackerEntryModel", back_populates="tracker")

    def __str__(self):
        return "%u Tracker: %s (%s), user %s (%u)" % (int(self.id), str(
            self.name), str(self.dimension), str(self.owner.username), int(self.owner_id))

    @staticmethod
    def has_owner(self):
        return True

    def check_owner(self, id):
        return self.owner_id == id


class TrackerEntryModel(db.Model):
    __tablename__ = "TrackerEntries"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    value = db.Column(db.Float, nullable=False)

    unit_id = db.Column(db.Integer, db.ForeignKey(
        "UnitIndex.id"), nullable=False)
    unit = db.relationship("UnitModel", foreign_keys="TrackerEntryModel.unit_id")

    parent_tracker_id = db.Column(
        db.Integer, db.ForeignKey("TrackerIndex.id"), nullable=False)
    tracker = db.relationship("TrackerModel", back_populates="entries",
                              foreign_keys="TrackerEntryModel.parent_tracker_id")

    def __str__(self):
        return "%u Tracker Entry: %s %s, tracker (%u) @ %s" % (int(self.id), str(
            self.value), str(self.unit.abbreviation), int(self.parent_tracker_id), str(self.time))

    @staticmethod
    def has_owner(self):
        return True

    # Returns True is the given user id is considered the owner of this
    # tracker entry
    def check_owner(self, id):
        return self.tracker.check_owner(id)
