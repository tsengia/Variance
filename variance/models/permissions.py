import logging
from variance import db


class PermissionModel(db.Model):
    __tablename__ = "PermissionIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Action that is permitted. (Ex: tracker.entry.new)
    action = db.Column(db.String(100), nullable=False)

    # Allow all users with this role to perform this action. (Ex: admin)
    allow_role = db.Column(db.String(20), nullable=True)

    # Allow the given user ID to perform this action.
    allow_user = db.Column(db.Integer, db.ForeignKey(
        "UserIndex.id"), nullable=True)

    # If set to true, the perms will check to make sure that the action is being performed by the user that owns the given database row entry
    # Ownership is tracked by the "owner" property
    allow_owner = db.Column(db.Boolean, nullable=True)

    # If set to true, the perms will check to make sure that the action being performed is on a row that has is_public set to True
    # Example: Some Recipes can be public for everyone to view, others are
    # private
    check_public = db.Column(db.Boolean, nullable=True)

    # If set to true, this action can be performed by ANY client.
    # Example: Viewing the list of units
    # Usually just used for view actions
    force_public = db.Column(db.Boolean, nullable=True)

    # For debugging and CLI purposes
    def __str__(self):
        return "Perm ID %5i: %25s - r(%s), u(%s), o(%s), cp(%s), fp(%s)" % (int(self.id),
                                                                            str(self.action),
                                                                            str(self.allow_role),
                                                                            str(self.allow_user),
                                                                            str(self.allow_owner),
                                                                            str(self.check_public),
                                                                            str(self.force_public))

    # Validation process:
    # Get all rows with the target action
    # For each row: If user fits into 1 row, then return True
    # If user does not fit into any rows, return False

    # Parameters: user  - the UserModel of the user that is performing the action
    #             model - the SQLAlchemyModel of what is being modified
    def check_user(self, user, model):
        if self.force_public is not None:
            return self.force_public

        if user:  # If the client is not logged in, then it's ok to pass False instead of a UserModel
            if self.allow_user is not None:
                if self.allow_user == user.id:
                    return True

            if self.allow_role is not None:
                if self.allow_role == user.role:
                    return True

            if self.allow_owner is not None:  # If the model is able to have an owner, then check if the owner matches the current user id
                if model:  # If the model has not been loaded yet then we cannot check for an owner
                    if model.has_owner() and model.check_owner(user.id):
                        return True
                # TODO: Make a log somewhere to notify dev that we attempted to
                # check owner of a None model

        if self.check_public is not None:
            if model:  # If the model has not been loaded yet then we cannot check for an owner
                if model.is_public:
                    return True
            # TODO: Make a log somewhere to notify dev that we attempted to
            # check owner of a None model

        return False
