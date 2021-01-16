from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.nutrition import MicronutrientModel, RecipeModel, ConsumableModel

class MicronutrientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MicronutrientModel
        load_instance = False

class RecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeModel
        load_instance = False

class ConsumableSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ConsumableModel
        load_instance = False