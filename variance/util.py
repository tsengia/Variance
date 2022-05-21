from marshmallow import Schema, validates, ValidationError, fields


def validate_unique(value, field_name, model, errmsg):
    """
    This function decorator checks to see if there are any instances of `model` in the database that
    have `field_name` set to `value`.
    Example: Checking is any UserModel's have their username set to "new_username".
    """
    def validate_unique_inner(view):
        def validate_unique_wrapped(*args, **kwargs):
            unique = False
            # TODO: Perform a query on the model to check if the field is unique.
            if not unique:
                abort(400, message={"error":errmsg})

            return view(*args, **kwargs)
        return validate_unique_wrapped
    return validate_unique_inner
