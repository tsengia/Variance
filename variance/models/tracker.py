from datetime import datetime
from variance import db
from variance.models import user.UserModel
from variance.models import unit.UnitModel

class TrackerModel(db.Model):
    __tablename__ = "TrackerIndex"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    dimension = db.Column(db.String(20), nullable=False)
    
    user = db.relationship("UserModel", back_populates="trackers")
    entries = db.relationship("TrackerEntry", back_populates="tracker")

class TrackerEntry(db.Model):
    __tablename__ = "TrackerEntries"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    value = db.Column(db.Float, nullable=False)
    unit_id = db.Column(db.Integer, ForeignKey(UnitModel.id), nullable=False)
    
    unit = db.relationship("UnitModel", foreign_keys="TrackerEntry.unit_id")
    tracker = db.relationship("TrackerModel", back_populates="entries")