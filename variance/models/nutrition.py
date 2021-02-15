from datetime import datetime
from variance import db

class NutrientModel(db.Model):
    __tablename__ = "NutrientIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Display Name of the Nutrient
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    scientific_name = db.Column(db.String(100), nullable=True)
    
    abbreviation = db.Column(db.String(50), nullable=True)
    
    description = db.Column(db.Text, nullable=True)

    # External databases info
    # FoodData Central Nutrient ID
    fdc_nid = db.Column(db.Integer, nullable=True)
    
    # FNDDS Nutrient Code
    fndds = db.Column(db.Integer, nullable=True)

class ConsumableNutrientsModel(db.Model):
    __tablename__ = "ConsumableNutrientsIndex"
    
    consumable_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"), nullable=False, primary_key=True)
    nutrient_id = db.Column(db.Integer, db.ForeignKey("NutrientIndex.id"), nullable=False, primary_key=True)
    measure_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    measure_value = db.Column(db.Float, nullable=False)
    
    measure_unit = db.relationship("UnitModel", foreign_keys="ConsumableNutrientsModel.measure_unit_id")
    nutrient = db.relationship("NutrientModel", foreign_keys="ConsumableNutrientsModel.nutrient_id")
    consumable = db.relationship("ConsumableModel", foreign_keys="ConsumableNutrientsModel.consumable_id")

class RecipieIngredientList(db.Model):
    __tablename__ = "RecipieIngredientList"
    
    recipe_id = db.Column(db.Integer, db.ForeignKey("RecipeIndex.id"), nullable=False, primary_key=True)
    measure_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    measure_value = db.Column(db.Float, nullable=False)
    consumable_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"), nullable=False, primary_key=True)
    
    recipe = db.relationship("RecipeModel", foreign_keys="RecipieIngredientList.recipe_id")
    measure_unit = db.relationship("UnitModel", foreign_keys="RecipieIngredientList.measure_unit_id")
    consumable = db.relationship("ConsumableModel", foreign_keys="RecipieIngredientList.consumable_id")

class RecipeModel(db.Model):
    __tablename__ = "RecipeIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the recipe
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # When was this recipe created?
    created_date = db.Column(db.Date, nullable=False, default=datetime.now)
    
    # Description about what this recipe is
    description = db.Column(db.Text, nullable=True)
    
    # Instructions on how to prepare this recipe
    instructions = db.Column(db.Text, nullable=True)
    
    # The consumable created by this recipie
    #result_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"), nullable=False)
    #result = db.relationship("ConsumableModel", foreign_keys="RecipeIndex.result_id")
    
    # How many servings of the consumable are produced by one serving of the recipe?
    recipe_yield = db.Column(db.Float, nullable=True)
    
    # If set to true, all users can see this ingredient
    public = db.Column(db.Boolean, nullable=False, default=False)
    
    # The user who added this recipie to the database
    created_by_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    created_by = db.relationship("UserModel", back_populates="recipies")
    
    # Attribution. AKA: Citation, license name, links, etc.
    attribution = db.Column(db.Text, nullable=True)
    
    # Who created this recipie? Or where was this recipe pulled from?
    author = db.Column(db.String(50), nullable=True)
    
class ConsumableModel(db.Model):
    __tablename__ = "ConsumableIndex"

    id = db.Column(db.Integer, primary_key=True)
    
    ### Management Info
    # Name of the consumable
    name = db.Column(db.String(100), unique=True, nullable=False)

    # When was this consumable created?
    created_date = db.Column(db.Date, nullable=False, default=datetime.now)

    # Description about what this consumable is
    description = db.Column(db.Text, nullable=True)

    # The user who added this consumable to the database
    created_by_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    created_by = db.relationship("UserModel", back_populates="consumables")

    # If set to true, all users can see this consumable
    public = db.Column(db.Boolean, nullable=False, default=False)

    ### Nutritional Info
    # Amount of calories (kcal) in 1 serving of this consumable
    calories = db.Column(db.Float, nullable=False, default=0)

    # Amount of protein (grams) in 1 serving of this consumable
    protein = db.Column(db.Float, nullable=False, default=0)

    # Amount of carbohydrates (grams) in 1 serving of this consumable
    carbohydrates = db.Column(db.Float, nullable=False, default=0)

    # Amount of fats (grams) in 1 serving of this consumable
    fat = db.Column(db.Float, nullable=False, default=0)
    
    # Does this consumable contain peanuts?
    has_peanuts = db.Column(db.Boolean, nullable=True)
    
    # Does this consumable contain treenuts?
    has_treenuts = db.Column(db.Boolean, nullable=True)
    
    # Does this consumable contain dairy?
    has_dairy = db.Column(db.Boolean, nullable=True)
    
    # Does this consumable contain eggs?
    has_eggs = db.Column(db.Boolean, nullable=True)
    
    # Does this consumable contain pork?
    has_pork = db.Column(db.Boolean, nullable=True)
    
    # Does this consumable contain beef (cow)?
    has_beef = db.Column(db.Boolean, nullable=True)
    
    # Does this consumable contain meat?
    has_meat = db.Column(db.Boolean, nullable=True)
    
    # Does this consumable contain fish?
    has_fish = db.Column(db.Boolean, nullable=True)
    
    # Does this consumable contain shellfish?
    has_shellfish = db.Column(db.Boolean, nullable=True)
    
    # Does this consumable contain gluten?
    has_gluten = db.Column(db.Boolean, nullable=True)
    
    # Is this consumable vegetarian?
    is_vegetarian = db.Column(db.Boolean, nullable=True)
    
    # Is this consumable vegan?
    is_vegan = db.Column(db.Boolean, nullable=True)
    
    # Is this consumable kosher?
    is_kosher = db.Column(db.Boolean, nullable=True)
    
    ### Storage, Packaging and Cost
    # Shelf life while still not opened (fridgerated or shelf) in days
    closed_shelf_life = db.Column(db.Integer, nullable=True)
    
    # Shelf life once opened in days (fridgerated or on shelf)
    opened_shelf_life = db.Column(db.Integer, nullable=True)
    
    # Freezer life (how many days this can last in a freezer)
    freezer_life = db.Column(db.Integer, nullable=True)
    
    # Does this consumable come in a package? (aka, meats, cookies, bread)
    is_packaged = db.Column(db.Boolean, nullable=True)
    
    # The most recent cost of buying 1 package of this consumable
    cost_per_package = db.Column(db.Float, nullable=True)
    
    # The number of servings in 1 package of this consumable
    servings_per_package = db.Column(db.Float, nullable=True)
    
    ### Organizational/sorting/filtering info
    # Is this consumable a brand name item?
    branded = db.Column(db.Boolean, nullable=False, default=False)
    
    # Is this consumable a raw ingredient? (raw meats, fruits, veggies, seasonings, etc.)
    is_ingredient = db.Column(db.Boolean, nullable=True)
    
    # Can this consumable be considered a snack?
    is_snack = db.Column(db.Boolean, nullable=True)
    
    # Is this consumable the result of a recipie?
    is_recipie = db.Column(db.Boolean, nullable=True)
    
    # Would this consumable be considered a main course for a meal?
    is_entree = db.Column(db.Boolean, nullable=True)
    
    # Would this consumable be considered a side course for a meal?
    is_side = db.Column(db.Boolean, nullable=True)
    
    # Would this consumable be considered a fruit? (raw fruits, fruit salads, etc.)
    is_fruit = db.Column(db.Boolean, nullable=True)
    
    # Would this consumable be considered a vegetable? (raw veggies, sauteed, baked, etc.)
    is_vegetable = db.Column(db.Boolean, nullable=True)
    
    # Would this consumable be considered a meat? (fried meats, breaded meat, grilled, etc.)
    is_meat = db.Column(db.Boolean, nullable=True)
    
    # Would this consumable be considered a soup? (stews count as well)
    is_soup = db.Column(db.Boolean, nullable=True)

    ### Identifiers & Attribution
    # Attribution. AKA: Citation, license name, links, etc.
    attribution = db.Column(db.Text, nullable=True)

    # Short display name of where this entry came from. Set to a value if ingested from another database
    data_source = db.Column(db.String(70), nullable=True)

    # External database IDs
    fdc_id = db.Column(db.Integer, nullable=True)
    fndds_id = db.Column(db.Integer, nullable=True)
    wweia_category = db.Column(db.Integer, nullable=True)
    upc = db.Column(db.String(20), nullable=True)
    upc_a = db.Column(db.Integer, nullable=True)
    upc_e = db.Column(db.Integer, nullable=True)
    ean_8 = db.Column(db.Integer, nullable=True)
    ean_13 = db.Column(db.Integer, nullable=True)