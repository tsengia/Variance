"""
Module for creating and tracking meal plans.
"""

from datetime import datetime
from variance.extensions import db

class ConsumedEntryModel(db.Model):
    "Model for consumption entries (tracking what was ate and when)"
    __tablename__ = "ConsumedEntryIndex"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(60), nullable=False)
    "Name of the food that was consumed."

    time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    "Time when this entry was made"

    owner_id = db.Column(db.Integer, db.ForeignKey(
        "UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", back_populates="consumption_entries")
    "The user who added this mealplan to the database"

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
    consumable_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"))
    "ID of the ConsumableModel that was consumed/ate/drank"

    consumable = db.relationship("ConsumableModel")
    "ConsumableModel that the user consumed/ate/drank"

    @staticmethod
    def has_owner() -> bool:
        return True

    def check_owner(self, id) -> bool:
        return self.owner_id == id

    def __str__(self) -> str:
        return "%u ConsumedEntryModel: %s @ %s, o(%u), c(%u)" % (
            self.id, self.name, str(self.time), self.owner_id, self.consumable_id)


class MealPlanModel(db.Model):
    "Representation of a meal plan. Mean plans have multiple days, and each day has multiple meals."
    __tablename__ = "MealPlanIndex"

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(60), unique=True, nullable=False)
    "Display name of this meal plan"

    description = db.Column(db.Text, nullable=True)
    "Description of this mealplan"

    is_public = db.Column(db.Boolean, nullable=False, default=False)
    "If set to true, all users can see this ingredient"

    owner_id = db.Column(db.Integer, db.ForeignKey(
        "UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", back_populates="mealplans")
    "The user who added this mealplan to the database"

    days = db.relationship("MealPlanDayModel", back_populates="mealplan")
    "List of days that this meal plan has."    

    @staticmethod
    def has_owner() -> bool:
        return True

    def check_owner(self, id) -> bool:
        return self.owner_id == id


class MealPlanDayModel(db.Model):
    "Representation of a single day within a mealplan. Each day can have multiple meals."
    __tablename__ = "MealPlanDayIndex"

    id = db.Column(db.Integer, primary_key=True)

    daynumber = db.Column(db.Integer, nullable=False, default=0)
    """Sequential order of when this day occurs in the mealplan. No order = 0, First day of the plan = 1, Second meal of the plan = 2"""

    parent_mealplan_id = db.Column(
        db.Integer, db.ForeignKey("MealPlanIndex.id"), nullable=False)
    mealplan = db.relationship("MealPlanModel", back_populates="days")
    "The MealPlan that this day belongs to"

    meals = db.relationship("MealModel", back_populates="mealday")
    "List of meals in this day"

    @staticmethod
    def has_owner() -> bool:
        return True

    def check_owner(self, id) -> bool:
        return self.mealplan.check_owner(id)


class MealModel(db.Model):
    "Representation of a single meal within a mealplan."
    __tablename__ = "MealIndex"

    id = db.Column(db.Integer, primary_key=True)

    mealnumber = db.Column(db.Integer, nullable=False, default=0)
    """Sequential order of when this meal is eaten. No order = 0, First meal of day = 1, Second meal of day = 2"""

    mealtime = db.Column(db.Time, nullable=True)
    "Optional: Approximate time that this meal should be eaten at"

    parent_mealday_id = db.Column(db.Integer, db.ForeignKey(
        "MealPlanDayIndex.id"), nullable=False)
    mealday = db.relationship("MealPlanDayModel", back_populates="meals")
    "Parent mealday that this meal exists in"

    @staticmethod
    def has_owner() -> bool:
        return True

    def check_owner(self, id) -> bool:
        return self.mealday.check_owner(id)
