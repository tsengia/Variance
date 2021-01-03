from context import variance
from variance.units import *
from unittest import TestCase

class TestConstructor(TestCase):
    def test_exceptions(self):
        with self.assertRaises(TypeError):
            m = Measure()
        with self.assertRaises(TypeError):
            m = Measure(20)
        with self.assertRaises(TypeError):
            m = Measure(20, "sadfg")
        with self.assertRaises(TypeError):
            m = Measure("hello", "sadfg")
        with self.assertRaises(TypeError):
            m = Measure("hello", MassUnit.GRAM)
        with self.assertRaises(TypeError):
            m = Grams(Miles(20))

class TestUnitConversions(TestCase):
    def test_cm_to_m(self):
        self.assertEqual(Meters(1), Meters(Centimeters(100)))

    def test_in_to_ft(self):
        self.assertEqual(Feet(1), Feet(Inches(12)))
        self.assertEqual(Feet(0), Feet(Inches(0)))

    def test_ft_to_yd(self):
        self.assertEqual(Yards(1), Yards(Feet(3)))
        
    def test_kcal_to_j(self):
        self.assertEqual(Jewels(4184000), Jewels(Calories(1000)))

class TestMassConversions(TestCase):
    def test_lb_to_kg(self):
        self.assertEqual(Pounds(20), Pounds(Kilograms(9.071847)))
        self.assertEqual(Pounds(1), Pounds(Kilograms(0.4535924)))

class TestComparisons(TestCase):
    def test_equal(self):
        self.assertEqual(Pounds(40) == Kilograms(Pounds(40)), True)
        self.assertEqual(Grams(1000) == Kilograms(1), True)
        self.assertEqual(Grams(10.2) == 10.2, False)
        self.assertEqual(float(Grams(10.2)), 10.2)
        self.assertEqual(Miles(20) == Liters(20), False)

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
        
    def test_right(self):
        p1 = Calories(100)
        self.assertEqual(200 + p1, 300)
        p2 = Gills(2.4)
        self.assertEqual(12.3 - p2, 9.9)

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
        
    def test_string(self):
        self.assertEqual(str(Meters(20)), "20.0 meters")
        self.assertEqual(str(Jewels(1.2)), "1.2 jewels")
        self.assertEqual(str(Gallons(0.75)), "0.75 gallons")

class TestParsing(TestCase):
    def test_integers(self):
        self.assertEqual(Cups(10), MeasurementParser.parse("10 cups"))
        self.assertEqual(Cups(5), MeasurementParser.parse("5cups"))
        self.assertEqual(FluidOunces(20), MeasurementParser.parse("20 fl. oz."))
        self.assertEqual(Liters(14), MeasurementParser.parse("14Liters"))

    def test_fractions(self):
        self.assertEqual(Milliliters(0.333), MeasurementParser.parse("1/3 mL"))
        self.assertEqual(Teaspoons(0.75), MeasurementParser.parse("3/4 tsp"))
        self.assertEqual(Liters(0.5), MeasurementParser.parse("1/2 liters"))
        self.assertEqual(Jewels(0.25), MeasurementParser.parse("1/4Jewel"))

    def test_floats(self):
        self.assertEqual(Meters(2.0), MeasurementParser.parse("2.000 m"))
        self.assertEqual(Centimeters(50.2), MeasurementParser.parse("50.2 centimeters"))
        self.assertEqual(Miles(4.2), MeasurementParser.parse("4.2 mi"))
        self.assertEqual(Grams(0.55), MeasurementParser.parse("0.55 g"))

    def test_failures(self):
        self.assertEqual(None, MeasurementParser.parse("sdfgm"))
        self.assertEqual(None, MeasurementParser.parse("hello world"))
        self.assertEqual(None, MeasurementParser.parse("barg 5"))
        self.assertEqual(None, MeasurementParser.parse("20.0.1 meters"))
        self.assertEqual(None, MeasurementParser.parse("20 snuffle wumps"))
