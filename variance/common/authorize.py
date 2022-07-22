"""
Collection of helper functions for authorization.
"""

from flask_smorest import abort

# Internal function that checks to see if there are any permission entries
# that permit the user/client to perform the action
def authorize_user(user, action, model) -> bool:
    """
    Returns True if the user is authorized to perform the action on the
    given model, False otherwise.
    """
    # TODO: Implement this
    return True


def authorize_user_or_abort(user, action, model):
    """
    Calls authorize_user() and aborts with a 401 message if the user is not
    authorized to perform the action on the given model.
    """
    allowed = authorize_user(user, action, model)

    if not allowed:
        # TODO: Log an error
        abort(401, message={"error": "You are not authorized to perform this action!"})
