from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.permissions import PermissionModel


class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PermissionModel
        load_instance = False
