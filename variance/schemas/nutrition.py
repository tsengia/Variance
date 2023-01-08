from marshmallow_sqlalchemy import auto_field
from variance.models.nutrition import NutrientInfoModel, RecipeModel, ConsumableModel, RecipeIngredientList, RecipeProductsList
from variance.schemas.resource import ResourceBaseSchema

class NutrientInfoSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = NutrientInfoModel

class RecipeIngredientSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = RecipeIngredientList

class RecipeProductSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = RecipeProductsList

class RecipeSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = RecipeModel


class ConsumableSchema(ResourceBaseSchema):
    uuid = auto_field(dump_only=True)
    class Meta:
        model = ConsumableModel
