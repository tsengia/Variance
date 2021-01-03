from unittest import TestCase
from context import variance
from variance.body import *

class TestSex(TestCase):
    def test_str(self):
        m = Sex.MALE
        self.assertEqual(str(m), "male")
        f = Sex.FEMALE
        self.assertEqual(str(f), "female")

class TestBMI(TestCase):
    def test_bmi(self):
        sex = Sex.MALE
        age = 20
        height = Feet(5) + Inches(9)
        weight = Pounds(185)
        b = Body(sex, age, height, weight)
        self.assertEqual(round(b.bmi, 1), 27.3)
        self.assertEqual(b.get_bmi_category(), "Overweight")
