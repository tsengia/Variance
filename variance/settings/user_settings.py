
from variance.extensions import db
from variance.settings.keyvalue import define_user_key_value_model

from variance.models.user import UserModel
from variance.models.unit import UnitModel

user_unit_settings = \
    define_user_key_value_model(\
        db.ForeignKey("UnitIndex.uuid", ondelete="CASCADE"),\
        "user_unit_settings")
