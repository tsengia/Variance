from datetime import datetime
from variance import db

class MicronutrientModel(db.Model):
    __tablename__ = "MicronutrientIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the micronutrient
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

class IngredientModel(db.Model):
    __tablename__ = "IngredientIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the ingredient
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Amount of calories (kcal) in 1 serving of this ingredient
    calories = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of protein (grams) in 1 serving of this ingredient
    protein = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of carbohydrates (grams) in 1 serving of this ingredient
    carbohydrates = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of fats (grams) in 1 serving of this ingredient
    fat = db.Column(db.Float, nullable=False, default=0)
    
    serving_size_value = db.Column(db.Float, nullable=False)
    serving_size_unit_id = db.Column(db.Integer, ForeignKey(UnitModel.id), nullable=False)
    
    serving_size_unit = db.relationship("UnitModel", foreign_keys="IngredientModel.serving_size_unit_id")
    
    # If set to true, all users can see this ingredient
    public = db.Column(db.Boolean, nullable=False, default=False)
    
    # The user who added this ingredient to the database
    created_by = db.relationship("UserModel", back_populates="ingredients")
    
    # Beyond here are other optional properties
    cost_per_package = db.Column(db.Float, nullable=True)
    servings_per_package = db.Column(db.Float, nullable=True)
    
    usda_id = db.Column(db.String(120), nullable=True)
    
class RecipieModel(db.Model):
    __tablename__ = "RecipieIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the recipie
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Who created this recipie? Or where was this recipie pulled from?
    author = db.Column(db.String(50), nullable=True)
    
    # Attribution. AKA: Citation, license name, links, etc.
    attribution = db.Column(db.Text, nullable=False)
    
    # When was this recipie created?
    created_date = db.Column(db.Date, nullable=False, default=datetime.now)
    
    # Description about what this recipie is
    description = db.Column(db.Text, nullable=True)
    
    # Instructions on how to prepare this recipie
    instructions = db.Column(db.Text, nullable=True)
    
    # Amount of calories (kcal) in 1 serving of this recipie
    calories = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of protein (grams) in 1 serving of this recipie
    protein = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of carbohydrates (grams) in 1 serving of this recipie
    carbohydrates = db.Column(db.Float, nullable=False, default=0)
    
    # Amount of fats (grams) in 1 serving of this recipie
    fat = db.Column(db.Float, nullable=False, default=0)
    
    # If set to true, all users can see this ingredient
    public = db.Column(db.Boolean, nullable=False, default=False)
    
    # The user who added this recipie to the database
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
    created_by = db.relationship("UserModel", back_populates="consumables")
    
    # Optional things
    cost_per_package = db.Column(db.Float, nullable=True)
    servings_per_package = db.Column(db.Float, nullable=True)
    
    usda_id = db.Column(db.String(120), nullable=True)