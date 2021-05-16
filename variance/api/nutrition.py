from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.nutrition import MicronutrientModel, IngredientModel, RecipieModel, ConsumableModel


class MicronutrientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MicronutrientModel
        load_instance = False


class IngredientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MicronutrientModel
        load_instance = False


class RecipieSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MicronutrientModel
        load_instance = False


class ConsumableSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MicronutrientModel
        load_instance = False
