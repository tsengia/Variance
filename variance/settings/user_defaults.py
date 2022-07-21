
from variance.extensions import db
from variance.common.keyvalue import define_user_key_value_model

from variance.models.user import UserModel
from variance.models.unit import UnitModel

user_unit_defaults = \
    define_user_key_value_model(\
        db.ForeignKey("UnitIndex.id", ondelete="CASCADE"),\
        "user_unit_defaults")
