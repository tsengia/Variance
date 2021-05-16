from datetime import datetime
from variance import db

class NutrientInfoModel(db.Model):
    __tablename__ = "NutrientInfoIndex"
    # This holds non-macro nutritional information about foods. 
    # Non-macros means that there should be no "Total Carbs" or "Total Fats" in here
    # Things such as "100mg of Vitamin C" belongs here, with the NutritionalInfoModel being "Vitamin C"
    # This is a very wide and vauge collection, because specific nutritional information can be spotty.

    id = db.Column(db.Integer, primary_key=True)

    # Display Name of the nutrition label (common name)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # If this nutrition label is about a specific molecule/element, then give the scientific name here
    scientific_name = db.Column(db.String(100), nullable=True)

    abbreviation = db.Column(db.String(50), nullable=True)

    # What does this nutrition label tell us?
    description = db.Column(db.Text, nullable=True)

    # Is this nutrient label an amino acid? (Ex: Tryptophan)
    is_amino_acid = db.Column(db.Boolean, nullable=True)
    
    # Is this nutrient label an element? (Ex: Iron, Magnesium, Nitrogen)
    is_element = db.Column(db.Boolean, nullable=True)
    
    # Is this nutrient a vitamin family or a member of a vitamin family? (Ex: Total Vitamin B, Vitamin B12, Retinol
    is_vitamin = db.Column(db.Boolean, nullable=True)
    
    # If this is a vitamin, what vitamin family does this belong to? (Ex: A, B, C, D...)
    vitamin_family = db.Column(db.String(2), nullable=True)
    
    # If this is a vitamin, is it a specific vitamin, and if so, what number? (Ex: Vitamin B12 would have 12 here)
    vitamin_number = db.Column(db.Integer, nullable=True)

    # External databases info
    # Wikipedia Link
    wikipedia_link = db.Column(db.String(200), nullable=True)
    
    # FoodData Central Nutrient ID
    fdc_nid = db.Column(db.String(20), nullable=True)

    # FNDDS Nutrient Code
    fndds = db.Column(db.String(20), nullable=True)
    
    @staticmethod
    def has_owner():
        return False
        
    def get_tags(self):
        a = []
        if self.is_amino_acid:
            a.append("amino acid")
        elif self.is_element:
            a.append("element")
        elif self.is_vitamin:
            if not self.vitamin_family is None:
                a.append("vitamin-" + str(self.vitamin_family))
            else:
                a.append("vitamin")
        return str(a)
        
    def __str__(self):
        return "%u NutrientInfoModel: %s %s" % (self.id, self.name, self.get_tags())

class ConsumableNutrientsModel(db.Model):
    __tablename__ = "ConsumableNutrientsIndex"
    # Associates consumables with their nutritional information (other than macros)
    consumable_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"), nullable=False, primary_key=True)
    nutrient_id = db.Column(db.Integer, db.ForeignKey("NutrientInfoIndex.id"), nullable=False, primary_key=True)
    measure_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    measure_value = db.Column(db.Float, nullable=False)

    measure_unit = db.relationship("UnitModel", foreign_keys="ConsumableNutrientsModel.measure_unit_id")
    nutrient = db.relationship("NutrientInfoModel", foreign_keys="ConsumableNutrientsModel.nutrient_id")
    consumable = db.relationship("ConsumableModel", foreign_keys="ConsumableNutrientsModel.consumable_id")

class RecipeIngredientList(db.Model):
    __tablename__ = "RecipeIngredientList"
    # Associates recipies with the consumables used by it as ingredients
    recipe_id = db.Column(db.Integer, db.ForeignKey("RecipeIndex.id"), nullable=False, primary_key=True)
    measure_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    measure_value = db.Column(db.Float, nullable=False)
    consumable_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"), nullable=False, primary_key=True)
    
    recipe = db.relationship("RecipeModel", foreign_keys="RecipeIngredientList.recipe_id")
    measure_unit = db.relationship("UnitModel", foreign_keys="RecipeIngredientList.measure_unit_id")
    consumable = db.relationship("ConsumableModel", foreign_keys="RecipeIngredientList.consumable_id")

class RecipeProductsList(db.Model):
    __tablename__ = "RecipeProductsList"
    # Associates 1 recipie with the multiple/single consumables it produces, along with the number of servings of consumable it produces
    recipe_id = db.Column(db.Integer, db.ForeignKey("RecipeIndex.id"), nullable=False, primary_key=True)
    servings = db.Column(db.Float, nullable=False, default=1)
    consumable_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"), nullable=False, primary_key=True)
    
    recipe = db.relationship("RecipeModel", foreign_keys="RecipeProductsList.recipe_id")
    product = db.relationship("ConsumableModel", foreign_keys="RecipeProductsList.consumable_id")

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

    # If set to true, all users can see this ingredient
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    
    # The user who added this recipie to the database
    owner_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", back_populates="recipies")
    
    ingredients = db.relationship("ConsumableModel", secondary="RecipeIngredientList")
    products = db.relationship("ConsumableModel", secondary="RecipeProductsList")
    
    @staticmethod
    def has_owner():
        return True
        
    def check_owner(self, id):
        return self.owner_id == id
    
    def __str__(self):
        return "%u RecipeModel: %s, public($s), %u(%s)" % (self.id, self.name, str(self.is_public), self.owner.id, self.owner.username)
    
    # Attribution. AKA: Citation, license name, links, etc.
    attribution = db.Column(db.Text, nullable=True)
    
    # Who (name of person) created this recipie? Or where was this recipe pulled from?
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
    owner_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", back_populates="consumables")

    @staticmethod
    def has_owner():
        return True
    
    def check_owner(self, id):
        return self.owner_id == id

    def __str__(self):
        return "%u ConsumableModel: %s, o(%u, %s), public(%s)" % (self.id, self.name, self.owner.id, self.owner.username, str(self.is_public))

    # If set to true, all users can see this consumable
    is_public = db.Column(db.Boolean, nullable=False, default=False)

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
    # Shelf life while original packaging is still not opened (fridgerated or shelf) in days
    closed_shelf_life = db.Column(db.Integer, nullable=True)
    
    # Shelf life once original packaging is opened in days (fridgerated or on shelf)
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
    # Is this a generic food? Ie. Sliced bread, chicken thigh, apple, etc. Useful for recipies
    # generic != branded
    is_generic = db.Column(db.Boolean, nullable=False, default=False)
    
    # Is this consumable a brand name item?
    is_branded = db.Column(db.Boolean, nullable=False, default=False)
    # If this is a branded food, what is the generic consumable? (Ex: Bakery cookie would point to a generic cookie consumable)
    generic_food_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"), nullable=True)
    generic_food = db.relationship("ConsumableModel", foreign_keys="ConsumableModel.generic_food_id")
    
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