"""
Collection of helper functions for authorization (permissions).
"""

from flask_smorest import abort
from marshmallow import Schema, validates, ValidationError, fields

from variance.models.permissions import PermissionModel

# Internal function that checks to see if there are any permission entries
# that permit the user/client to perform the action
def authorize_user(user, action, model) -> bool:
    """
    Checks the permission tables to see if the given user is authorized
    to perform the given action.

    If the user has no identity (ie. not logged in), then user can be
    set to False.
    The model that the user is performing the action is needed to check
    ownership.

    Returns True if the user is authorized to perform the action on the
    given model, False otherwise.
    """
    a = PermissionModel.query.filter_by(action=action)
    for p in a:
        if p.check_user(user, model):
            return True
    # TODO: Make log to notify dev if no perm entries for that action can be
    # found
    return False


def authorize_user_or_abort(user, action, model):
    """
    Calls authorize_user() and aborts with a 401 message if the user is not
    authorized to perform the action on the given model.
    """
    allowed = check_perms(user, action, model)

    if not allowed:
        # TODO: Log an error
        abort(401, message={"error": "You do not have permission to perform this action!"})
