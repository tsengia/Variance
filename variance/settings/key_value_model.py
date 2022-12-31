from variance.extensions import db
from variance.models.user import UserModel

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

def define_key_value_model(value_type: object, table_name: str):

    class KeyValueModel(db.Model):
        "Template model for generating key-value tables for global preferences"

        __tablename__ = table_name

        key = db.Column(db.String(40), 
                nullable=False, primary_key=True)
        "String that this entry is accessed by."
        
        value = db.Column(value_type, nullable=False)
        "Value of this key."