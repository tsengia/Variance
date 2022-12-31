
from variance.extensions import db
from variance.settings.key_value_model import define_key_value_model

from variance.models.unit import UnitModel
from variance.models.user import UserModel


# TODO: Test that check_owner works
# TODO: Test to make sure entries are deleted when users are deleted

def define_user_key_value_model(value_type: object, table_name: str):
    "Helper function to declare a key-value table for storing user preferences"

    class UserKeyValueModel(db.Model):
        "Template model for generating key-value tables for user preferences"
        # TODO: Proper authorization
        __tablename__ = table_name

        user = db.Column(db.String(36),
                db.ForeignKey("UserIndex.uuid", ondelete="CASCADE"), 
                nullable=False, primary_key=True)
        "User that this key-value entry is for."

        key = db.Column(db.String(40), 
                nullable=False, primary_key=True)
        "String that this entry is accessed by."
        
        value = db.Column(value_type, nullable=False)
        "Value of this key."



user_unit_settings = \
    define_user_key_value_model(\
        db.ForeignKey("UnitIndex.uuid", ondelete="CASCADE"),\
        "user_unit_settings")

user_number_settings = \
    define_key_value_model(\
        db.Float(), "user_number_settings")

user_string_settings = \
    define_key_value_model(\
        db.String(length=40), "user_string_settings")

user_boolean_settings = \
    define_key_value_model(\
        db.Boolean(), "user_boolean_settings")
