from marshmallow import Schema, validates, ValidationError, fields
from flask_smorest import abort

def validate_unique(value, model, field, errmsg):
    """
    This function decorator checks to see if there are any instances of `model` in the database that
    have `field_name` set to `value`.
    Example: Checking is any UserModel's have their username set to "new_username".
    """
    unique = not (model.query.filter(field == value).first() is not None)
    if not unique:
        abort(409, message=errmsg)
