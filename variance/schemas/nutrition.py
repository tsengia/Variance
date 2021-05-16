from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.nutrition import NutrientModel, RecipeModel, ConsumableModel


class NutrientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NutrientModel
        load_instance = False


class RecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeModel
        load_instance = False


class ConsumableSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ConsumableModel
        load_instance = False
