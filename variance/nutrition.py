from datetime import datetime
from enum import Enum
from .body import Body, Sex
from .units import *
from .series import DataSeries

class Nutrient():
    pass

class MacroNutrient(Nutrient, Enum):
    PROTEIN = 4
    CARBOHYDRATE = 4
    FAT = 9

    @staticmethod
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
