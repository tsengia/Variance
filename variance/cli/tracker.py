from variance.extensions import db

from variance.models.tracker import TrackerModel
from variance.schemas.tracker import TrackerSchema
from variance.cli.resource import ResourceCLI

tracker_cli = ResourceCLI(TrackerModel, TrackerSchema, "Tracker", "trackers")