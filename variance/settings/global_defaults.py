from variance.extensions import db
from variance.common.keyvalue import define_key_value_model

from variance.models.user import UserModel
from variance.models.unit import UnitModel

global_unit_defaults = \
    define_key_value_model(\
        db.ForeignKey("UnitIndex.id", ondelete="CASCADE"),\
        "global_unit_defaults")

global_number_defaults = \
    define_key_value_model(\
        db.Float(), "global_number_defaults")

global_string_defaults = \
    define_key_value_model(\
        db.String(length=40), "global_string_defaults")

global_boolean_defaults = \
    define_key_value_model(\
        db.Boolean(), "global_boolean_defaults")
