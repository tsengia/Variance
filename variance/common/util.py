from flask_smorest import abort

def validate_unique(value, model, field, errmsg):
    """
    Checks to see if there are any instances of `model` in the database that
    have `field_name` set to `value`.
    Example: Checking is any UserModel's have their username set to "new_username".

    Returns True if unique, False otherwise.
    """
    return not (model.query.filter(field == value).first() is not None)

def validate_unique_or_abort(value, model, field, errmsg):
    """
    Calls validate_unique() and aborts with a 409 message if there is an
    already existing model that has the given field set to the same value.
    """
    if not validate_unique(value, model, field, errmsg)
        abort(409, message=errmsg)
