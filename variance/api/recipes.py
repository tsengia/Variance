from variance.models.nutrition import RecipeModel, RecipeIngredientList, RecipeProductsList
from variance.schemas.nutrition import RecipeSchema, RecipeIngredientSchema, RecipeProductSchema
from variance.api.resource_api import VarianceCollection, VarianceChildResource

recipe_endpoint = VarianceCollection(RecipeModel, RecipeSchema, "recipes", "recipe")
recipe_ingredients_endpoint = VarianceChildResource(RecipeIngredientList, RecipeIngredientSchema, "recipes_ingredients", "ingredients", recipe_endpoint)
recipe_products_endpoint = VarianceChildResource(RecipeProductsList, RecipeProductSchema, "recipes_products", "products", recipe_endpoint)
