from datetime import datetime
from variance import db

class TrackerModel(db.Model):
    __tablename__ = "TrackerIndex"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    dimension = db.Column(db.String(20), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="trackers")
    
    
    entries = db.relationship("TrackerEntry", back_populates="tracker")

class TrackerEntry(db.Model):
    __tablename__ = "TrackerEntries"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    value = db.Column(db.Float, nullable=False)
    
    unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    unit = db.relationship("UnitModel", foreign_keys="TrackerEntry.unit_id")
    
    parent_tracker_id = db.Column(db.Integer, db.ForeignKey("TrackerIndex.id"), nullable=False)
    tracker = db.relationship("TrackerModel", back_populates="entries", foreign_keys="TrackerEntry.parent_tracker_id")