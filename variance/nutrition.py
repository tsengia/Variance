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
    pass

class MacroList():
    def fat(self, serving_size):
        return self._fat * serving_size

    def carbohydrate(self, serving_size):
        return self._carb * serving_size
    
    def protein(self, serving_size):
        return self._protein * serving_size

    def calories_from_macros(self, serving_size):
        total = MacroNutrient.calories_per_measurement(MacroNutrient.PROTEIN, self.protein(serving_size))
        total += MacroNutrient.calories_per_measurement(MacroNutrient.CARBOHYDRATE, self.carbohydrate(serving_size))
        total += MacroNutrient.calories_per_measurement(MacroNutrient.FAT, self.fat(serving_size))

        return total

    def __init__(self, protein_mass_per_serving, fat_mass_per_serving, carb_mass_per_serving):
        self._protein = Grams(protein_mass_per_serving)
        self._fat = Grams(fat_mass_per_serving)
        self._carb = Grams(carb_mass_per_serving)

class MicroList():
    def get_micro(self, micro_name, serving_size):
        return self.micros[micro_name] * serving_size

    def __init__(self):
        self.micros = {}

class NutrientTarget():
    def __init__(self):
        self.calories = Calories(0)
        self.protein = Grams(0)
        self.carbohydrates = Grams(0)
        self.fats = Grams(0)
