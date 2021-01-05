from .nutrition import MacroList

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