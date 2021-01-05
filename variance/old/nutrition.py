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
            raise TypeError("mass_measure passed to calories_per_measurement should be of MassMeasure type! Was passed a " + str(type(mass_measure)) + ": " + str(mass_measure))
        if not isinstance(macro_nutrient, MacroNutrient):
            raise TypeError("macro_nutrient passed to calories_per_measurement should be MacroNutrient type! Was passed: " + str(macro_nutrient))

        return Calories(macro_nutrient.value * Grams(mass_measure))

class MicroNutrient(Nutrient):
    def __init__(self, name):
        self.name = name

class MacroList():
    """
    Keeps track of the amount of macronutrients in 1 serving of something.
    """
    def calories_from_macros(self):
        total = MacroNutrient.calories_per_measurement(MacroNutrient.PROTEIN, self.protein)
        total += MacroNutrient.calories_per_measurement(MacroNutrient.CARBOHYDRATE, self.carbohydrate)
        total += MacroNutrient.calories_per_measurement(MacroNutrient.FAT, self.fat)

        return total

    def __init__(self, protein_mass_per_serving, carb_mass_per_serving, fat_mass_per_serving):
        self.protein = Grams(protein_mass_per_serving)
        self.fat = Grams(fat_mass_per_serving)
        self.carbohydrate = Grams(carb_mass_per_serving)

class NutrientTarget():
    def __init__(self):
        self.calories = Calories(0)
        self.protein = Grams(0)
        self.carbohydrates = Grams(0)
        self.fats = Grams(0)
