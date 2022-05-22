from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.nutrition import NutrientInfoModel, RecipeModel, ConsumableModel


class NutrientInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NutrientInfoModel
        load_instance = False


class RecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeModel
        load_instance = False


class ConsumableSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ConsumableModel
        load_instance = False
