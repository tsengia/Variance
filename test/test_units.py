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

class TestComparisons(TestCase):
    def test_equal(self):
        self.assertEqual(Pounds(40) == Kilograms(Pounds(40)), True)
        self.assertEqual(Grams(1000) == Kilograms(1), True)
        self.assertEqual(Grams(10.2) == 10.2, True)

    def test_less_than(self):
        self.assertEqual(Pounds(1) < Kilograms(1), True)
        self.assertEqual(Miles(1) < Kilometers(3), True)
        self.assertEqual(Jewels(20.3) < 21.7, True)

    def test_greater_than(self):
        self.assertEqual(Gallons(1) > Cups(1), True)
        self.assertEqual(Pounds(10) > Milligrams(200), True)
        self.assertEqual(Ounces(12.4) > 3.141, True)

class TestOperations(TestCase):
    def test_inplace(self):
        p1 = Pints(2)
        p1 += 2
        self.assertEqual(p1, Pints(4))
        p1 -= 1
        self.assertEqual(p1, Pints(3))
        p1 *= 5
        self.assertEqual(p1, Pints(15))
        p1 /= 3
        self.assertEqual(p1, Pints(5))

    def test_normal(self):
        p1 = Quarts(2)
        self.assertEqual(p1 * 6, Quarts(12))
        self.assertEqual(p1 + Quarts(3), Quarts(5))
        self.assertEqual(p1 / 2, Quarts(1))
        p2 = FluidOunces(24)
        self.assertEqual(p2 // 7, FluidOunces(3))
        self.assertEqual(p2 - FluidOunces(20), FluidOunces(4))

class TestCasts(TestCase):
    def test_int(self):
        self.assertEqual(int(Tablespoons(12.3)), 12)
        self.assertEqual(int(Jewels(23.4)), 23)
        self.assertEqual(int(Meters(4.3)), 4)
        self.assertEqual(int(Kilograms(1002.5)), 1002)
        self.assertEqual(int(VolumeUnit.MILLILITER), 1)
        self.assertEqual(int(MassUnit.GRAM), 1)
        self.assertEqual(int(LengthUnit.METER), 1)

    def test_float(self):
        self.assertEqual(float(Tablespoons(12)), 12.0)
        self.assertEqual(float(Jewels(23)), 23.0)
        self.assertEqual(float(Meters(4)), 4.0)
        self.assertEqual(float(Kilograms(1002)), 1002.0)


