from context import variance
from variance.units import *
from unittest import TestCase

class TestUnitConversions(TestCase):
    def test_cm_to_m(self):
        self.assertEqual(Meters(1), Meters(Centimeters(100)))

    def test_in_to_ft(self):
        self.assertEqual(Feet(1), Feet(Inches(12)))
        self.assertEqual(Feet(0), Feet(Inches(0)))

    def test_ft_to_yd(self):
        self.assertEqual(Yards(1), Yards(Feet(3)))

class TestMassConversions(TestCase):
    def test_lb_to_kg(self):
        self.assertEqual(Pounds(20), Pounds(Kilograms(9.071847)))
        self.assertEqual(Pounds(1), Pounds(Kilograms(0.4535924)))
