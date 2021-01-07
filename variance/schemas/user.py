from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.user import UserModel

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = False