from variance import db

class PermissionModel(db.Model):
    __tablename__ = "PermissionIndex"

    id = db.Column(db.Integer, primary_key=True)
    
    # Action that is permitted. (Ex: tracker.entry.new)
    action = db.Column(db.String(100), nullable=False)
    
    # Allow all users with this role to perform this action. (Ex: admin)
    allow_role = db.Column(db.String(20), nullable=True)
     
    # Allow the given user ID to perform this action.
    allow_user = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=True)
    
    # If set to true, the perms will check to make sure that the action is being performed by the user that owns the given database row entry
    # Ownership is tracked by the "owner" property
    allow_owner = db.Column(db.Boolean, nullable=True)
    
    # If set to true, the perms will check to make sure that the action being performed is on a row that has is_public set to True
    # Example: Some Recipes can be public for everyone to view, others are private
    check_public = db.Column(db.Boolean, nullable=True)
    
    # If set to true, this action can be performed by ANY client.
    # Example: Viewing the list of units
    # Usually just used for view actions
    force_public = db.Column(db.Boolean, nullable=True)
    
    # Validation process:
    # Get all rows with the target action
    # For each row: If user fits into 1 row, then return True
    # If user does not fit into any rows, return False
    
    # Parameters: user  - the UserModel of the user that is performing the action
    #             model - the SQLAlchemyModel of what is being modified
    def check_user(self, user, model):
        if not self.force_public is None:
            return self.force_public == True
        
        if user: # If the client is not logged in, then it's ok to pass False instead of a UserModel
            if not self.allow_user is None:
                if self.allow_user == user.id:
                    return True
        
            if not self.allow_role is None:
                if self.allow_role == user.role:
                    return True
                    
            if not self.allow_owner is None: # If the model is able to have an owner, then check if the owner matches the current user id
                if model.has_owner() and model.check_owner(user.id):
                    return True
                
        if not self.check_public is None:
            if model.is_public:
                return True
        
        return False