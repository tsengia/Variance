from variance.models.tracker import TrackerModel, TrackerEntryModel
from variance.schemas.tracker import TrackerSchema, TrackerEntrySchema
from variance.api.resource_api import VarianceResource

trackers_endpoint = VarianceResource(TrackerModel, TrackerSchema, __name__, "trackers")
# TODO: Make tracker entries a child resouce/path
#       ie. should be at /trackers/<tracker-id>/entries
