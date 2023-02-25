from variance.models.nutrition import RecipeModel, RecipeIngredientList, RecipeProductsList
from variance.schemas.nutrition import RecipeSchema, RecipeIngredientSchema, RecipeProductSchema
from variance.api.resource_api import VarianceResource

recipe_endpoint = VarianceResource(RecipeModel, RecipeSchema, "recipes", "recipe")
recipe_ingredients_endpoint = VarianceResource(RecipeIngredientList, RecipeIngredientSchema, "recipes_ingredients", "ingredients")
recipe_products_endpoint = VarianceResource(RecipeProductsList, RecipeProductSchema, "recipes_products", "products")
recipe_ingredients_endpoint.set_parent(recipe_endpoint)
recipe_products_endpoint.set_parent(recipe_endpoint)