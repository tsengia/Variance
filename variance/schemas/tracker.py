from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.tracker import TrackerModel, TrackerEntry

class TrackerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TrackerModel
        load_instance = False

class TrackerEntrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TrackerEntryModel
        load_instance = False