from unittest import TestCase
from context import variance
from variance.units import *
from variance.nutrition import *

class MacroNutrientTest(TestCase):
    def test_macro_enum(self):
        self.assertEqual(MacroNutrient.PROTEIN, MacroNutrient.PROTEIN)
        self.assertEqual(MacroNutrient.CARBOHYDRATE, MacroNutrient.CARBOHYDRATE)
        self.assertEqual(MacroNutrient.FAT, MacroNutrient.FAT)

    def test_calorie_conversion(self):
        self.assertEqual(MacroNutrient.calories_per_measurement(MacroNutrient.FAT, Grams(2)), Calories(18))
        with self.assertRaises(TypeError):
            MacroNutrient.calories_per_measurement(MacroNutrient.PROTEIN, "asdfg")
        with self.assertRaises(TypeError):
            MacroNutrient.calories_per_measurement(8, Grams(2))

    def test_nutrient_target_init(self):
        n = NutrientTarget()
        self.assertEqual(n.calories, Calories(0))
        self.assertEqual(n.protein, Grams(0))
        self.assertEqual(n.carbohydrates, Grams(0))
        self.assertEqual(n.fats, Grams(0))
