"""
Module for representing nutritional information
"""
from datetime import datetime
from variance.extensions import db, ResourceBase

class ConsumedEntryModel(ResourceBase):
    "Model for consumption entries (tracking what was ate and when)"
    __tablename__ = "ConsumedEntryIndex"

    name = db.Column(db.String(60), nullable=False)
    "Name of the food that was consumed."

    time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    "Time when this entry was made"

    # Nutritional Info
    calories = db.Column(db.Float, nullable=False, default=0)
    "Amount of calories consumed (grams)"

    protein = db.Column(db.Float, nullable=False, default=0)
    "Amount of protein consumed (grams)"

    carbohydrates = db.Column(db.Float, nullable=False, default=0)
    "Amount of carbohydrates consumed (grams)"

    fat = db.Column(db.Float, nullable=False, default=0)
    "Amount of fats consumed (grams)"

    # Linking to a Consumable
    servings = db.Column(db.Float, nullable=False, default=1)
    "Number of servings consumed"
    consumable_uuid = db.Column(db.String(36), db.ForeignKey("ConsumableIndex.uuid"))
    "ID of the ConsumableModel that was consumed/ate/drank"

    consumable = db.relationship("ConsumableModel")
    "ConsumableModel that the user consumed/ate/drank"

    def __str__(self) -> str:
        return "%s ConsumedEntryModel: %s @ %s, c(%u)" % (
            self.uuid, self.name, str(self.time), self.consumable_uuid)


class ConsumableNutrientsModel(ResourceBase):
    "Associates consumables with their nutritional information (other than macro-nutrients)"
    __tablename__ = "ConsumableNutrientsIndex"
    consumable_uuid = db.Column(db.String(36), db.ForeignKey(
        "ConsumableIndex.uuid"), nullable=False, primary_key=True)
    nutrient_uuid = db.Column(db.String(36), db.ForeignKey(
        "NutrientInfoIndex.uuid"), nullable=False, primary_key=True)
    measure_unit_uuid = db.Column(
        db.String(36), db.ForeignKey("UnitIndex.uuid"), nullable=False)
    measure_value = db.Column(db.Float, nullable=False)

    measure_unit = db.relationship(
        "UnitModel", foreign_keys="ConsumableNutrientsModel.measure_unit_uuid")
    nutrient = db.relationship(
        "NutrientInfoModel",
        foreign_keys="ConsumableNutrientsModel.nutrient_uuid")
    consumable = db.relationship(
        "ConsumableModel",
        foreign_keys="ConsumableNutrientsModel.consumable_uuid")


class RecipeIngredientList(ResourceBase):
    "Associates recipies with the consumables used by it as ingredients."
    __tablename__ = "RecipeIngredientList"
    recipe_uuid = db.Column(db.String(36), db.ForeignKey(
        "RecipeIndex.uuid"), nullable=False, primary_key=True)
    measure_unit_uuid = db.Column(
        db.String(36), db.ForeignKey("UnitIndex.uuid"), nullable=False)
    measure_value = db.Column(db.Float, nullable=False)
    consumable_uuid = db.Column(db.String(36), db.ForeignKey(
        "ConsumableIndex.uuid"), nullable=False, primary_key=True)

    recipe = db.relationship(
        "RecipeModel", foreign_keys="RecipeIngredientList.recipe_uuid", viewonly=True)
    measure_unit = db.relationship(
        "UnitModel", foreign_keys="RecipeIngredientList.measure_unit_uuid")
    consumable = db.relationship(
        "ConsumableModel", foreign_keys="RecipeIngredientList.consumable_uuid", viewonly=True)


class RecipeProductsList(ResourceBase):
    """Associates 1 Recipe with the multiple/single Consumables it produces,
    along with the number of servings of each Consumable it produces"""
    __tablename__ = "RecipeProductsList"
    
    recipe_uuid = db.Column(db.String(36), db.ForeignKey(
        "RecipeIndex.uuid"), nullable=False, primary_key=True)
    "ID of the Recipe that produces the product"
    
    recipe = db.relationship(
        "RecipeModel", foreign_keys="RecipeProductsList.recipe_uuid", 
        viewonly=True)
    "RecipeModel that produces the product"
    
    servings = db.Column(db.Float, nullable=False, default=1)
    "Number of servings of the product that 1 serving of the Recipe produces."    
    product_uuid = db.Column(db.String(36), db.ForeignKey(
        "ConsumableIndex.uuid"), nullable=False, primary_key=True)
    "ID of the Consumable this Recipe produces"
    product = db.relationship(
        "ConsumableModel", foreign_keys="RecipeProductsList.product_uuid",
        viewonly=True)
    "ConsumableModel that this Recipe produces"


class NutrientInfoModel(ResourceBase):
    """This holds non-macro nutritional information about foods.
    Non-macros means that there should be no "Total Carbs" or "Total Fats" in here
    Things such as "100mg of Vitamin C" belongs here, with the NutritionalInfoModel being "Vitamin C"
    This is a very wuuide and vauge collection, because specific nutritional
    information can be spotty.
    """
    __tablename__ = "NutrientInfoIndex"

    name = db.Column(db.String(100), nullable=False)
    "Display Name of the nutrition label"

    scientific_name = db.Column(db.String(100), nullable=True)
    """If this nutrition label is about a specific molecule/element, then give
    the scientific name here"""

    abbreviation = db.Column(db.String(50), nullable=True)

    description = db.Column(db.Text, nullable=True)
    "What does this nutrition label tell us?"

    is_amino_acuuid = db.Column(db.Boolean, nullable=True)
    "Is this nutrient label an amino acuuid? (Ex: Tryptophan)"

    is_element = db.Column(db.Boolean, nullable=True)
    "Is this nutrient label an element? (Ex: Iron, Magnesium, Nitrogen)"

    is_vitamin = db.Column(db.Boolean, nullable=True)
    """Is this nutrient a vitamin family or a member of a vitamin family? (Ex:
    Total Vitamin B, Vitamin B12, Retinol"""

    vitamin_family = db.Column(db.String(2), nullable=True)
    """If this is a vitamin, what vitamin family does this belong to? (Ex: A,
    B, C, D...)"""

    vitamin_number = db.Column(db.Integer, nullable=True)
    """If this is a vitamin, is it a specific vitamin, and if so, what number?
    (Ex: Vitamin B12 would have 12 here)"""

    # External databases info
    wikipedia_link = db.Column(db.String(200), nullable=True)
    "Wikipedia Link"

    fdc_nuuid = db.Column(db.String(20), nullable=True)
    "FoodData Central Nutrient ID"

    fndds = db.Column(db.String(20), nullable=True)
    "FNDDS Nutrient Code"

    def get_tags(self) -> str:
        a = []
        if self.is_amino_acuuid:
            a.append("amino acuuid")
        elif self.is_element:
            a.append("element")
        elif self.is_vitamin:
            if self.vitamin_family is not None:
                a.append("vitamin-" + str(self.vitamin_family))
            else:
                a.append("vitamin")
        return str(a)

    def __str__(self) -> str:
        return "%s NutrientInfoModel: %s %s" % (
            self.uuid, self.name, self.get_tags())

class RecipeModel(ResourceBase):
    __tablename__ = "RecipeIndex"
    
    name = db.Column(db.String(100), nullable=False)
    "Display name of the recipe"

    created_date = db.Column(db.Date, nullable=False, default=datetime.now)
    "Date and time when this Recipe was created."

    description = db.Column(db.Text, nullable=True)
    "Description about what this Recipe is"

    instructions = db.Column(db.Text, nullable=True)
    "Instructions on how to prepare this Recipe"

    ingredients = db.relationship(
        "ConsumableModel", secondary="RecipeIngredientList")
    "List of ingredients that this Recipe requires."
    products = db.relationship(
        "ConsumableModel", secondary="RecipeProductsList")
    "List of Consumables that this Recipe produces."
    
    attribution = db.Column(db.Text, nullable=True)
    "Attribution. AKA: Citation, license name, links, etc."

    author = db.Column(db.String(50), nullable=True)
    "Who (name of person) created this recipie? Or where was this recipe pulled from?"
    
    def __str__(self) -> str:
        return "%s RecipeModel: %s" % (
            self.uuid, self.name)

class ConsumableModel(ResourceBase):
    "Representation of an ingredient, food item, or result of a recipe that a user can consume/eat/drink"
    __tablename__ = "ConsumableIndex"

    # Management Info
    name = db.Column(db.String(100), nullable=False)
    "Display name of the consumable"

    created_date = db.Column(db.Date, nullable=False, default=datetime.now)
    "When was this consumable created?"

    description = db.Column(db.Text, nullable=True)
    "Description about what this consumable is"

    # Nutritional Info
    serving_size_unit_uuid = db.Column(db.String(36), db.ForeignKey(
        "UnitIndex.uuid"), nullable=False)
    serving_size_unit = db.relationship("UnitModel")
    "Unit for serving size measurement"
    serving_size_value = db.Column(db.Float, nullable=False)
    "Value for serving size measurement"

    calories = db.Column(db.Float, nullable=False, default=0)
    "Amount of calories (kcal) in 1 serving of this consumable"

    protein = db.Column(db.Float, nullable=False, default=0)
    "Amount of protein (grams) in 1 serving of this consumable"

    carbohydrates = db.Column(db.Float, nullable=False, default=0)
    "Amount of carbohydrates (grams) in 1 serving of this consumable"

    fat = db.Column(db.Float, nullable=False, default=0)
    "Amount of fats (grams) in 1 serving of this consumable"

    ### Storage, Packaging and Cost
    closed_shelf_life = db.Column(db.Integer, nullable=True)
    """Shelf life while original packaging is still not opened (fruuidgerated or
    shelf) in days"""

    opened_shelf_life = db.Column(db.Integer, nullable=True)
    """Shelf life once original packaging is opened in days (fruuidgerated or on
    shelf)"""

    freezer_life = db.Column(db.Integer, nullable=True)
    "Freezer life (how many days this can last in a freezer)"

    is_packaged = db.Column(db.Boolean, nullable=True)
    "Does this consumable come in a package? (aka, meats, cookies, bread)"

    cost_per_package = db.Column(db.Float, nullable=True)
    "The most recent cost of buying 1 package of this consumable"

    servings_per_package = db.Column(db.Float, nullable=True)
    "The number of servings in 1 package of this consumable"

    # Organizational/sorting/filtering info
    is_generic = db.Column(db.Boolean, nullable=False, default=False)
    """Is this a generic food? Ie. Sliced bread, chicken thigh, apple, etc. Useful for recipies
    generic != branded"""

    is_branded = db.Column(db.Boolean, nullable=False, default=False)
    "Is this consumable a brand name item?"
    generic_food_uuid = db.Column(db.String(36), db.ForeignKey(
        "ConsumableIndex.uuid"), nullable=True)
    generic_food = db.relationship(
        "ConsumableModel", foreign_keys="ConsumableModel.generic_food_uuid")
    """If this is a branded food, what is the generic consumable? (Ex: Bakery
    cookie would point to a generic cookie consumable)"""

    is_ingredient = db.Column(db.Boolean, nullable=True)
    """Is this consumable a raw ingredient? (raw meats, fruits, veggies,
    seasonings, etc.)"""

    is_recipie = db.Column(db.Boolean, nullable=True)
    "Is this consumable the result of a recipie?"

    ### Identifiers & Attribution
    attribution = db.Column(db.Text, nullable=True)
    "Attribution. AKA: Citation, license name, links, etc."

    data_source = db.Column(db.String(70), nullable=True)
    """Short display name of where this entry came from. Set to a value if
    ingested from another database"""

    # External database IDs
    fdc_uuid = db.Column(db.Integer, nullable=True)
    fndds_uuid = db.Column(db.Integer, nullable=True)
    wweia_category = db.Column(db.Integer, nullable=True)
    upc = db.Column(db.String(20), nullable=True)
    upc_a = db.Column(db.Integer, nullable=True)
    upc_e = db.Column(db.Integer, nullable=True)
    ean_8 = db.Column(db.Integer, nullable=True)
    ean_13 = db.Column(db.Integer, nullable=True)

    def __str__(self) -> str:
        return "%s ConsumableModel: %s" % (
            self.uuid, self.name)
