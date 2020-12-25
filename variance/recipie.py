from .units import *
from .nutrition import *
from .consumable import Consumable

class Ingredient():
    """
        Ingredient class. Mostly just a placeholder that can be used in the future to make grocery lists and hold shopping information, and to calculate macros/micros for recipies.

        The serving_measure gives scale to how much of each macro and micro is in an ingredient. For example, 1 ounce of FooBird meat has 20 grams of protein in it. In this case, the macros.protein would be set to Grams(20), and the serving_measure set to Ounces(1). This way, when findig the amount of protein in half an ounce of FooBird meat, we can simply take Grams(20) * (Ounces(0.5)/Ounces(1)) to get Grams(10). The same goes for micros.
    
        micros is simply a dictionary. The key values are strings representing the name of the micronutrient, and the value stored is a MassMeasure representing how much of that micronutrient is present in 1 serving.
    """
    def __init__(self, name, serving_measure, macros=MacroList(0,0,0), micros={}):
        self.name = name
        self.serving_measure = serving_measure
        self.macros = macros
        self.micros = micros

class Recipie(Consumable):
    """
    Recipie class, a type of Consumable. Has an ingredient list and instructions for how to make this recipie. Nutrition information can be calculated from ingredients, or manually entered. Ingredients list is an array of two element tuples: The ingredient, and the measurement of that ingredient for one serving.
    """
    def add_ingredient(self, ingredient, measurement):
        self.ingredients.append((ingredient, measurement))

    def set_calories_per_serving(self, calories_per_serving):
        self.manual_calories = True
        self.__calories_per_serving = calories_per_serving

    def calories(self, serving_size):
        if self.manual_calories:
            return self.__calories_per_serving * serving_size
        else:
            return self.macros.calories_from_macros(serving_size)

    def __get_macro_list(self):
        if self.manual_macrolist: # If the user hardcoded a list, use it. Otherwise calculate from ingredients
            return self.__macrolist
        else:
            self.__macrolist = MacroList(0,0,0)
            for ingredient, measure in self.ingredients:
                self.__macrolist._protein += ingredient.macros.protein(measure / ingredient.serving_measure)
                self.__macrolist._carb += ingredient.macros.carbohydrate(measure / ingredient.serving_measure)
                self.__macrolist._fat += ingredient.macros.fat(measure / ingredient.serving_measure)
            return self.__macrolist

    def __set_macro_list(self, new_list):
        self.__macrolist = new_list
        self.manual_macrolist = False

    def __get_micro_list(self):
        if self.manual_microlist:
            return self.__microlist
        else:
            self.__microlist = {}
            for ingredient, measure in self.ingredients:
                for mic, mass in ingredient.micros:
                    if mic in self.__microlist:
                        self.__microlist[mic] += mass
                    else:
                        self.__microlist[mic] = mass
            return self.__microlist

    def __set_micro_list(self, new_list):
        self.manual_microlist = True
        self.__microlist = new_list

    def __init__(self, name):
        self.name = name
        self.description = ""
        self.instructions = ""
        self.ingredients = []

        # Boolean flags set to True if the user/program manually set the calorie/macros/micros amounts instead of calculating them from ingredients
        self.manual_macrolist = False
        self.manual_microlist = False
        self.manual_calories = False
        self.__macrolist = None
        self.__microlist = None
        self.__calories_per_serving = None

        self.macros = property(__get_macro_list, __set_macro_list)
        self.micros = property(__get_micro_list, __set_micro_list)
