from marshmallow_sqlalchemy import auto_field
from variance.models.user import UserModel
from variance.schemas.resource import ResourceBaseSchema

class UserSchema(ResourceBaseSchema):
    """
    User schema that contains everything about a user.
    """
    uuid = auto_field(dump_only=True) 
    
    class Meta:
        model = UserModel
