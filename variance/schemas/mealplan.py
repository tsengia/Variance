from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.mealplan import MealPlanModel, MealPlanDayModel, MealModel

class MealPlanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MealPlanModel
        load_instance = False
        
class MealPlanDaySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MealPlanDayModel
        load_instance = False
        
class MealSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MealModel
        load_instance = False