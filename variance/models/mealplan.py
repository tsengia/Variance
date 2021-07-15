from datetime import datetime
from variance.extensions import db


class ConsumedEntryModel(db.Model):
    __tablename__ = "ConsumedEntryIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the food that was consumed.
    name = db.Column(db.String(60), nullable=False)

    # Time when this entry was made
    time = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    # The user who added this mealplan to the database
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", back_populates="consumption_entries")

    # Nutritional Info
    # Amount of calories consumed (grams)
    calories = db.Column(db.Float, nullable=False, default=0)

    # Amount of protein consumed (grams)
    protein = db.Column(db.Float, nullable=False, default=0)

    # Amount of carbohydrates consumed (grams)
    carbohydrates = db.Column(db.Float, nullable=False, default=0)

    # Amount of fats consumed (grams)
    fat = db.Column(db.Float, nullable=False, default=0)

    # Linking to a Consumable
    servings = db.Column(db.Float, nullable=False, default=1)
    consumable_id = db.Column(db.Integer, db.ForeignKey("ConsumableIndex.id"))

    consumable = db.relationship("ConsumableModel")

    @staticmethod
    def has_owner():
        return True

    def check_owner(self, id):
        return self.owner_id == id

    def __str__(self):
        return "%u ConsumedEntryModel: %s @ %s, o(%u), c(%u)" % (
            self.id, self.name, str(self.time), self.owner_id, self.consumable_id)


class MealPlanModel(db.Model):
    __tablename__ = "MealPlanIndex"

    id = db.Column(db.Integer, primary_key=True)
    # Management Info
    # Name of this meal plan
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # If set to true, all users can see this ingredient
    is_public = db.Column(db.Boolean, nullable=False, default=False)

    # The user who added this mealplan to the database
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "UserIndex.id"), nullable=False)
    owner = db.relationship("UserModel", back_populates="mealplans")

    days = db.relationship("MealPlanDayModel", back_populates="mealplan")
    
    @staticmethod
    def has_owner():
        return True

    def check_owner(self, id):
        return self.owner_id == id


class MealPlanDayModel(db.Model):
    __tablename__ = "MealPlanDayIndex"

    id = db.Column(db.Integer, primary_key=True)

    # What day in the meal plan is this? First day == 1, no order = 0
    daynumber = db.Column(db.Integer, nullable=False, default=0)

    # What mealplan does this belong to?
    parent_mealplan_id = db.Column(
        db.Integer, db.ForeignKey("MealPlanIndex.id"), nullable=False)
    mealplan = db.relationship("MealPlanModel", back_populates="days")

    # List of meals in this day
    meals = db.relationship("MealModel", back_populates="mealday")

    @staticmethod
    def has_owner():
        return True

    def check_owner(self, id):
        return self.mealplan.check_owner(id)


class MealModel(db.Model):
    __tablename__ = "MealIndex"

    id = db.Column(db.Integer, primary_key=True)

    # What meal in the day is this? First meal == 1, no order = 0
    mealnumber = db.Column(db.Integer, nullable=False, default=0)

    # Around what time is this meal eaten?
    mealtime = db.Column(db.Time, nullable=True)

    # Parent mealday that this meal exists in
    parent_mealday_id = db.Column(db.Integer, db.ForeignKey(
        "MealPlanDayIndex.id"), nullable=False)
    mealday = db.relationship("MealPlanDayModel", back_populates="meals")

    @staticmethod
    def has_owner():
        return True

    def check_owner(self, id):
        return self.mealday.check_owner(id)
