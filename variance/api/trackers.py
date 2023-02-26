from variance.models.tracker import TrackerModel, TrackerEntryModel
from variance.schemas.tracker import TrackerSchema, TrackerEntrySchema
from variance.api.resource_api import VarianceCollection, VarianceChildResource

trackers_endpoint = VarianceCollection(TrackerModel, 
                                       TrackerSchema, 
                                       "trackers", 
                                       "trackers")

tracker_entries_endpoint = VarianceChildResource(TrackerEntryModel, 
                                       TrackerEntrySchema,
                                       "tracker_entries", 
                                       "entries",
                                       trackers_endpoint)