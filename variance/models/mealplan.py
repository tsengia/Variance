"""
Module for creating and tracking meal plans.
"""

from datetime import datetime
from variance.extensions import db

class MealPlanModel(db.Model):
    "Representation of a meal plan. Mean plans have multiple days, and each day has multiple meals."
    __tablename__ = "MealPlanIndex"

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(60), unique=True, nullable=False)
    "Display name of this meal plan"

    description = db.Column(db.Text, nullable=True)
    "Description of this mealplan"

    days = db.relationship("MealPlanDayModel", back_populates="mealplan")
    "List of days that this meal plan has."    

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

