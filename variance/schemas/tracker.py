from marshmallow_sqlalchemy import auto_field
from variance.models.tracker import TrackerModel, TrackerEntryModel
from variance.schemas.resource import ResourceBaseSchema

class TrackerSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = TrackerModel

class TrackerEntrySchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)

    class Meta:
        model = TrackerEntryModel