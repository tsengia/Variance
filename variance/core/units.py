from enum import Enum
from copy import copy
import re

class Unit:
    pass

class MassUnit(Unit, Enum):
    # The value of the enum is: value * measurement = measurement_in_grams
    # So the value of the enum is the coefficient used to convert from the enum unit to grams
    GRAM = (1,("g", "gram", "grams"), "mass")
    POUND = (453.5924,("lb", "lbs", "pound", "pounds"),"mass")
    OUNCE = (28.34952,("oz", "ounce", "ounces"),"mass")
    KILOGRAM = (1000,("kg", "kilogram", "kilograms"),"mass")
    MILLIGRAM = (0.001, ("mg", "milligram", "milligrams"),"mass")
    STONE = (0, ("st", "stone"), "mass")

    def __str__(self):
        return self.value[1][-1]

    def __int__(self):
        return int(self.value[0])

    def __float__(self):
        return float(self.value[0])

    __repr__ = __str__

        
class LengthUnit(Unit, Enum):
    METER = (1,("m", "meter", "meters"),"length")
    CENTIMETER = (0.01,("cm", "centimeter", "centimeters"),"length")
    FOOT = (0.3048,("ft", "foot", "feet"),"length")
    INCH = (0.0254,("in", "inch", "inches"),"length")
    YARD = (0.9144,("yd", "yard", "yards"),"length")
    KILOMETER = (1000,("km", "kilometer", "kilometers"),"length")
    MILE = (1609.344,("mi", "mile", "miles"),"length")

    def __str__(self):
        return self.value[1][-1]

    def __int__(self):
        return int(self.value[0])

    def __float__(self):
        return float(self.value[0])

    __repr__ = __str__

class EnergyUnit(Unit, Enum):
    CALORIE = (1,("Cal", "kcal", "kilocalorie","kilocalories","Calorie","Calories"), "energy") # NOTE: This is Food Calories. So 1 Cal == 1000calories
    JEWEL = (0.00023900573614,("J", "jewel", "jewels"),"energy") 

    def __str__(self):
        return self.value[1][-1]

    def __int__(self):
        return int(self.value[0])

    def __float__(self):
        return float(self.value[0])

    __repr__ = __str__

class VolumeUnit(Unit, Enum):
    MILLILITER = (1,("mL", "ml", "milli-liter", "milli-liters", "milliliter", "milliliters"),"volume")
    LITER = (1000, ("L", "liter", "liters"),"volume") 
    CUP = (240, ("cup", "cups"), "volume")
    QUART = (960, ("qt", "quart", "quarts"), "volume")
    GALLON = (3840, ("gal", "Gal", "gallon", "gallons"), "volume")
    PINT = (480, ("pt", "pint", "pints"), "volume") # 2 cups
    GILL = (120, ("gill", "gills"), "volume") # I swear if I ever have to use this unit... tally of times unit is used: 0
    FLUID_OUNCE = (30, ("fl oz", "fl. oz.", "fl-oz", "fl. oz", "fluid ounce", "fluid ounces"), "volume") # 1/8 of a cup
    TABLESPOON = (15, ("tbsp", "tablespoon", "tablespoons"), "volume")  # 1/16 of a cup
    TEASPOON = (5, ("tsp", "teaspoon", "teaspoons"), "volume") # 1/48 of a cup

    def __str__(self):
        return self.value[1][-1]

    def __int__(self):
        return int(self.value[0])

    def __float__(self):
        return float(self.value[0])

    __repr__ = __str__


class TimeUnit(Unit, Enum):
    SECOND = (1,("s", "sec","second","seconds"), "time")
    MINUTE = (60,("min", "minute", "minutes"),"time") 
    HOUR = (3600,("hr", "hour", "hours"), "time")

    def __str__(self):
        return self.value[1][-1]

    def __int__(self):
        return int(self.value[0])

    def __float__(self):
        return float(self.value[0])

    __repr__ = __str__

class SpeedUnit(Unit, Enum):
    METERS_PER_SECOND = (1,("m/s", "meters per second","meters/second"), "speed")
    MILES_PER_HOUR = (0.44704,("mph", "miles per hour", "miles/hour"),"speed") 
    KILOMETERS_PER_HOUR = (0.2777778,("kmph", "kilometers per hour", "kilometers/hour"), "speed")

    def __str__(self):
        return self.value[1][-1]

    def __int__(self):
        return int(self.value[0])

    def __float__(self):
        return float(self.value[0])

    __repr__ = __str__



class Measure():
    def __init__(self, value, unit, accuracy=6):
        if not isinstance(unit, Unit):
            raise TypeError("unit passed to Measure must be of type Unit!")
        self.unit = unit
        if isinstance(value, Measure): # TODO: Check that units are of the same dimensions
            if not value.unit.value[2] == self.unit.value[2]:
                raise TypeError("Measurement passed is not of the same unit type!")
            self.value = float(round(value.value * value.unit.value[0] / self.unit.value[0], accuracy))
        elif isinstance(value, (int, float)):
            self.value = float(value)
        else:
            raise TypeError("value passed to Measure must be int, float, or Measure type!")

    def __str__(self):
        return str(self.value) + " " + str(self.unit)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __eq__(self, rhs):
        if isinstance(rhs, Measure):
            # Check to make sure they measure the same thing (both are length, or mass or volume, etc.)
            if not rhs.unit.value[2] == self.unit.value[2]:
                return False
            c = Measure(rhs, self.unit, 3)
            return round(self.value, 3) == c.value
        else:
            return False

    def __gt__(self, rhs):
        if isinstance(rhs, (int, float)):
            c = float(rhs)
            return self.value > c
        elif isinstance(rhs, Measure):
            c = Measure(rhs, self.unit, 3)
            return self.value > c.value

    def __lt__(self, rhs):
        if isinstance(rhs, (int, float)):
            c = float(rhs)
            return self.value < rhs
        elif isinstance(rhs, Measure):
            c = Measure(rhs, self.unit, 3)
            return self.value < c.value

    def __mul__(self, rhs):
        com = Measure(rhs, self.unit)
        res = copy(self)
        res.value *= com.value
        return res

    def __truediv__(self, rhs):
        com = Measure(rhs, self.unit)
        res = copy(self)
        res.value /= com.value
        return res       

    def __floordiv__(self, rhs):
        com = Measure(rhs, self.unit)
        res = copy(self)
        res.value = res.value // com.value
        return res

    def __sub__(self, rhs):
        com = Measure(rhs, self.unit)
        res = copy(self)
        res.value -= com.value
        return res

    def __add__(self, rhs):
        com = Measure(rhs, self.unit)
        res = copy(self)
        res.value += com.value
        return res        

    def __iadd__(self, rhs):
        self.value += Measure(rhs, self.unit).value
        return self

    def __isub__(self, rhs):
        self.value -= Measure(rhs, self.unit).value
        return self

    def __imul__(self, rhs):
        self.value *= Measure(rhs, self.unit).value
        return self

    def __itruediv__(self, rhs):
        self.value /= Measure(rhs, self.unit).value
        return self

    ### TODO: Figure out what to do if LHS isn't an int or float...
    def __rmul__(self, lhs):
        if isinstance(lhs, (int, float)):
            return self.value * lhs

    def __radd__(self, lhs):
        if isinstance(lhs, (int, float)):
            return self.value + lhs

    def __rsub__(self, lhs):
        if isinstance(lhs, (int, float)):
            return lhs - self.value

    __repr__ = __str__

class LengthMeasure(Measure):
    pass

class MassMeasure(Measure):
    pass

class TimeMeasure(Measure):
    pass

class EnergyMeasure(Measure):
    pass

class VolumeMeasure(Measure):
    pass

class Grams(MassMeasure):
    def __init__(self, measure):
        super().__init__(measure, MassUnit.GRAM)

class Milligrams(MassMeasure):
    def __init__(self, measure):
        super().__init__(measure, MassUnit.MILLIGRAM)

class Pounds(MassMeasure):
    def __init__(self, measure):
        super().__init__(measure, MassUnit.POUND)

class Kilograms(MassMeasure):
    def __init__(self, measure):
        super().__init__(measure, MassUnit.KILOGRAM)

class Ounces(MassMeasure):
    def __init__(self, measure):
        super().__init__(measure, MassUnit.OUNCE)

class Meters(LengthMeasure):
    def __init__(self, measure):
        super().__init__(measure, LengthUnit.METER)

class Centimeters(LengthMeasure):
    def __init__(self, measure):
        super().__init__(measure, LengthUnit.CENTIMETER)

class Feet(LengthMeasure):
    def __init__(self, measure):
        super().__init__(measure, LengthUnit.FOOT)

class Inches(LengthMeasure):
    def __init__(self, measure):
        super().__init__(measure, LengthUnit.INCH)

class Miles(LengthMeasure):
    def __init__(self, measure):
        super().__init__(measure, LengthUnit.MILE)

class Kilometers(LengthMeasure):
    def __init__(self, measure):
        super().__init__(measure, LengthUnit.KILOMETER)

class Yards(LengthMeasure):
    def __init__(self, measure):
        super().__init__(measure, LengthUnit.YARD)

class Calories(EnergyMeasure):
    def __init__(self, measure):
        super().__init__(measure, EnergyUnit.CALORIE)

class Jewels(EnergyMeasure):
    def __init__(self, measure):
        super().__init__(measure, EnergyUnit.JEWEL)

class Milliliters(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.MILLILITER)

class Liters(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.LITER)

class Cups(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.CUP)

class Pints(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.PINT)
        
class Gills(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.GILL)

class Quarts(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.QUART)

class Gallons(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.GALLON)

class Tablespoons(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.TABLESPOON)

class Teaspoons(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.TEASPOON)

class FluidOunces(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.FLUID_OUNCE)
        
class UnitParser():
    @staticmethod
    def parse(text):
        text = text.strip().lower().replace(".", "")

        for m in MassUnit:
            if text in m.value[1]:
                return m

        for v in VolumeUnit:
            if text in v.value[1]:
                return v

        for e in EnergyUnit:
            if text in e.value[1]:
                return e

        for l in LengthUnit:
            if text in l.value[1]:
                return l

class MeasurementParser():
    _measure_split_regex = re.compile("(?<=[0-9])[\s](?=([a-zA-Z.]+(\s[a-zA-Z]+[.]*)?))")
    _measure_space_regex = re.compile("([0-9])([a-zA-Z])")

    @staticmethod
    def parse(text):
        spaced_text = re.sub(MeasurementParser._measure_space_regex, r"\1 \2", text) # Put a space between the value and units if there wasn't one already
        s = MeasurementParser._measure_split_regex.split(spaced_text) # split at the space between the value and the unit
        if len(s) < 2:
            return None # Failed to parse a measurement from this, return None
        if len(s) > 2:
            s = s[0:2]

        try:
            if "/" in s[0]: # value is a fraction....
                numerator, denominator = s[0].split("/")
                value = round(float(numerator) / float(denominator), 3)
            else:
                value = float(s[0])
        except ValueError:
            return None

        unit = UnitParser.parse(s[1])
        if not unit:
            return None
        
        return Measure(value, unit)
