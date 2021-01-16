from datetime import datetime
from variance import db

class MicronutrientModel(db.Model):
    __tablename__ = "MicronutrientIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the micronutrient
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
class RecipeMicroNutrientsModel(db.Model):
    __tablename__ = "RecipeMicroNutrientsIndex"
    
    recipe_id = db.Column(db.Integer, db.ForeignKey("RecipeIndex.id"), nullable=False, primary_key=True)
    micronutrient_id = db.Column(db.Integer, db.ForeignKey("MicronutrientIndex.id"), nullable=False, primary_key=True)
    measure_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    measure_value = db.Column(db.Float, nullable=False)
    
    measure_unit = db.relationship("UnitModel", foreign_keys="RecipeMicroNutrientsModel.measure_unit_id")
    micronutrient = db.relationship("MicronutrientModel", foreign_keys="RecipeMicroNutrientsModel.micronutrient_id")
    recipe = db.relationship("RecipeModel", foreign_keys="RecipeMicroNutrientsModel.recipe_id")

class ConsumableMicroNutrientsModel(db.Model):
    __tablename__ = "ConsumableMicroNutrientsIndex"
    
    consumable_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"), nullable=False, primary_key=True)
    micronutrient_id = db.Column(db.Integer, db.ForeignKey("MicronutrientIndex.id"), nullable=False, primary_key=True)
    measure_unit_id = db.Column(db.Integer, db.ForeignKey("UnitIndex.id"), nullable=False)
    measure_value = db.Column(db.Float, nullable=False)
    
    measure_unit = db.relationship("UnitModel", foreign_keys="ConsumableMicroNutrientsModel.measure_unit_id")
    micronutrient = db.relationship("MicronutrientModel", foreign_keys="ConsumableMicroNutrientsModel.micronutrient_id")
    consumable = db.relationship("ConsumableModel", foreign_keys="ConsumableMicroNutrientsModel.consumable_id")

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
    
    # Who created this recipie? Or where was this recipe pulled from?
    author = db.Column(db.String(50), nullable=True)
    
    # Attribution. AKA: Citation, license name, links, etc.
    attribution = db.Column(db.Text, nullable=False)
    
    # When was this recipe created?
    created_date = db.Column(db.Date, nullable=False, default=datetime.now)
    
    # Description about what this recipe is
    description = db.Column(db.Text, nullable=True)
    
    # Instructions on how to prepare this recipe
    instructions = db.Column(db.Text, nullable=True)
    
    # Amount of calories (kcal) in 1 serving of this recipe
    calories = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of protein (grams) in 1 serving of this recipe
    protein = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of carbohydrates (grams) in 1 serving of this recipe
    carbohydrates = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of fats (grams) in 1 serving of this recipe
    fat = db.Column(db.Float, nullable=False, default=0)
    
    # If set to true, all users can see this ingredient
    public = db.Column(db.Boolean, nullable=False, default=False)
    
    # The user who added this recipie to the database
    created_by_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    created_by = db.relationship("UserModel", back_populates="recipies")
    
    #Optional things
    usda_id = db.Column(db.String(120), nullable=True)
    
class ConsumableModel(db.Model):
    __tablename__ = "ConsumableIndex"
    
    id = db.Column(db.Integer, primary_key=True)

    # Name of the consumable
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # When was this consumable created?
    created_date = db.Column(db.Date, nullable=False, default=datetime.now)
    
    # Description about what this consumable is
    description = db.Column(db.Text, nullable=True)
    
    # Amount of calories (kcal) in 1 serving of this consumable
    calories = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of protein (grams) in 1 serving of this consumable
    protein = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of carbohydrates (grams) in 1 serving of this consumable
    carbohydrates = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of fats (grams) in 1 serving of this consumable
    fat = db.Column(db.Float, nullable=False, default=0)
    
    # If set to true, all users can see this consumable
    public = db.Column(db.Boolean, nullable=False, default=False)
    
    # The user who added this consumable to the database
    created_by_id = db.Column(db.Integer, db.ForeignKey("UserIndex.id"), nullable=False)
    created_by = db.relationship("UserModel", back_populates="consumables")
    
    # Optional things
    cost_per_package = db.Column(db.Float, nullable=True)
    servings_per_package = db.Column(db.Float, nullable=True)
    
    usda_id = db.Column(db.String(120), nullable=True)