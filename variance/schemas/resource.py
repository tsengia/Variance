from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class ResourceBaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = False
