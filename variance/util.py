from flask import g
from flask_smorest import abort
from marshmallow import Schema, validates, ValidationError, fields

from variance.models.permissions import PermissionModel

def validate_unique(value, model, field, errmsg):
    """
    This function decorator checks to see if there are any instances of `model` in the database that
    have `field_name` set to `value`.
    Example: Checking is any UserModel's have their username set to "new_username".
    """
    unique = not (model.query.filter(field == value).first() is not None)
    if not unique:
        abort(409, message=errmsg)

# Internal function that checks to see if there are any permission entries
# that permit the user/client to perform the action
def _check_perms(action, user, model):
    a = PermissionModel.query.filter_by(action=action)
    for p in a:
        if p.check_user(user, model):
            return True
    # TODO: Make log to notify dev if no perm entries for that action can be
    # found
    return False


def check_perms(action, model):
    def inner_wrap(view):
        def wrapped_view(*args, **kwargs):
            allowed = False
            if not g.user:
                allowed = _check_perms(action, False, model)
            else:
                allowed = _check_perms(action, g.user, model)

            if not allowed:
                # TODO: Log an error
                abort(
                    401, message={
                        "error": "You do not have permission to perform this action!"})

            return view(*args, **kwargs)
        return wrapped_view
    return inner_wrap
