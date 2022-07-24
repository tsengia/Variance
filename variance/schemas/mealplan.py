from marshmallow_sqlalchemy import auto_field
from variance.models.mealplan import MealPlanModel, MealPlanDayModel, MealModel
from variance.schemas.resource import ResourceBaseSchema


class MealPlanSchema(ResourceBaseSchema):
    class Meta:
        model = MealPlanModel

    uuid = auto_field(dump_only=True)


class MealPlanDaySchema(ResourceBaseSchema):
    class Meta:
        model = MealPlanDayModel

    uuid = auto_field(dump_only=True)


class MealSchema(ResourceBaseSchema):
    class Meta:
        model = MealModel

    uuid = auto_field(dump_only=True)
