from datetime import datetime
from enum import Enum
from .body import Body, Sex
from .units import *
from .series import DataSeries

class Metabolism():

    # Below is the Katch-McArdle formula for resting daily energy expenditure
    @staticmethod
    def rdee(body):
        return Calories(370 + (21.6 * float(Kilograms(user.lean_body_mass))))

    # Below is the Mifflin St. Jeor equation for basal metabolic rate
    @staticmethod
    def bmr(body):
        if body.sex == Sex.MALE:
            sex_modifier = 5
        elif body.sex == Sex.FEMALE:
            sex_modifier = -161

        return Calories(float(10*Kilograms(body.weight)) + float(6.25*Centimeters(body.height)) - float(5 * body.age) + sex_modifier)

class Nutrient():
    pass

class MacroNutrient(Nutrient, Enum):
    PROTEIN = 4
    CARBOHYDRATE = 4
    FAT = 9

    def calories_per_measurement(macro_nutrient, mass_measure):
        if not isinstance(mass_measure, MassMeasure):
            raise TypeError("mass_measure passed to calories_per_measurement should be of MassMeasure type!")
        if not isinstance(macro_nutrient, MacroNutrient):
            raise TypeError("macro_nutrient passed to calories_per_measurement should be MacroNutrient type!")

        return Calories(macro_nutrient.value * Grams(mass_measure))

class MicroNutrient(Nutrient, Enum):
    pass

class NutrientTarget():
    def __init__(self):
        self.calories = Calories(0)
        self.protein = Grams(0)
        self.carbohydrates = Grams(0)
        self.fats = Grams(0)
