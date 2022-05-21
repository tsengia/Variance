from marshmallow import Schema, validates, ValidationError, fields
from flask_smorest import abort

def validate_unique(value, field_name, model, errmsg):
    """
    This function decorator checks to see if there are any instances of `model` in the database that
    have `field_name` set to `value`.
    Example: Checking is any UserModel's have their username set to "new_username".
    """
    def validate_unique_inner(view):
        def validate_unique_wrapped(*args, **kwargs):
            unique = not model.query.filter(model[field_name] == value[field_name]).exists()
            if not unique:
                abort(400, message=errmsg)

            return view(*args, **kwargs)
        return validate_unique_wrapped
    return validate_unique_inner
