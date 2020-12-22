from enum import Enum

class Unit:
    pass

class MassUnit(Unit, Enum):
    # The value of the enum is: value * measurement = measurement_in_grams
    # So the value of the enum is the coefficient used to convert from the enum unit to grams
    GRAM = (1,"g","m")
    POUND = (453.5924,"lb","m")
    OUNCE = (28.34952,"oz","m")
    KILOGRAM = (1000,"kg","m")
    MILLIGRAM = (0.001, "mg","m")

    def __str__(self):
        return self.value[1]

    def __int__(self):
        return self.value[0]

    @staticmethod
    def get_unit_from_abbreviation(abbrv):
        if abbrv == "g":
            return MassUnit.GRAM
        if abbrv == "lb":
            return MassUnit.POUND
        if abbrv == "kg":
            return MassUnit.KILOGRAM
        if abbrv == "oz":
            return MassUnit.OUNCE
        if abbrv == "mg":
            return MassUnit.MILLIGRAM

    @staticmethod
    def get_abbreviation_list():
        return ["g","lb","oz","kg","mg"]

    __repr__ = __str__

        
class LengthUnit(Unit, Enum):
    METER = (1,"m","l")
    CENTIMETER = (0.01,"cm","l")
    FOOT = (0.3048,"ft","l")
    INCH = (0.0254,"in","l")
    YARD = (0.9144,"yd","l")
    KILOMETER = (1000,"km","l")
    MILE = (1609.344,"mi","l")

    def __str__(self):
        return self.value[1]

    def __int__(self):
        return self.value[0]

    @staticmethod
    def get_unit_from_abbreviation(abbrv):
        if abbrv == "m":
            return LengthUnit.METER
        elif abbrv == "cm":
            return LengthUnit.CENTIMETER
        if abbrv == "ft":
            return LengthUnit.FOOT
        if abbrv == "in":
            return LengthUnit.INCH
        if abbrv == "yd":
            return LengthUnit.YARD
        if abbrv == "km":
            return LengthUnit.KILOMETER
        if abbrv == "mi":
            return LengthUnit.MILE

    @staticmethod
    def get_abbreviation_list():
        return ["m","cm","ft","in","yd","km","mi"]

    __repr__ = __str__

class EnergyUnit(Unit, Enum):
    CALORIE = (1,"Cal","e") # NOTE: This is Food Calories. So 1 Cal == 1000calories
    JEWEL = (4184,"J","e") 

    def __str__(self):
        return self.value[1]

    def __int__(self):
        return self.value[0]

    @staticmethod
    def get_unit_from_abbreviation(abbrv):
        if abbrv == "Cal":
            return EnergyUnit.CALORIE
        elif abbrv == "J":
            return EnergyUnit.JEWEL

    @staticmethod
    def get_abbreviation_list():
        return ["J","Cal"]

    __repr__ = __str__

class VolumeUnit(Unit, Enum):
    MILLILETER = (1,"ml","v")
    LITER = (1000, "L","v") 
    CUP = (240, "cup", "v")
    QUART = (960, "qt", "V")
    GALLON = (3840, "gal", "v")
    PINT = (480, "pt", "v") # 2 cups
    GILL = (120, "gill", "v") # I swear if I ever have to use this unit... tally of times unit is used: 0
    FLUID_OUNCE = (30, "fl oz", "v") # 1/8 of a cup
    TABLESPOON = (15, "tbsp", "v")  # 1/16 of a cup
    TEASPOON = (5, "tsp", "v") # 1/48 of a cup

    def __str__(self):
        return self.value[1]

    def __int__(self):
        return self.value[0]

    @staticmethod
    def get_unit_from_abbreviation(abbrv):
        if abbrv == "ml":
            return EnergyUnit.MILLILETER
        elif abbrv == "L":
            return VolumeUnit.LITER
        elif abbrv == "cup":
            return VolumeUnit.CUP
        elif abbrv == "qt":
            return VolumeUnit.QUART
        elif abbrv == "gal":
            return VolumeUnit.GALLON
        elif abbrv == "pt":
            return VolumeUnit.PINT
        elif abbrv == "gill":
            return VolumeUnit.GILL
        elif abbrv == "fl oz" or abbrv == "fl. oz." or abbrv == "fl. oz":
            return VolumeUnit.FLUID_OUNCE
        elif abbrv == "tbsp" or abbrv == "Tbsp":
            return VolumeUnit.TABLESPOON
        elif abbrv == "tsp":
            return VolumeUnit.TEASPOON

    @staticmethod
    def get_abbreviation_list():
        return ["ml", "L", "cup", "qt", "gal", "pt", "gill", "fl oz", "tbsp", "tsp"]

    __repr__ = __str__

class Measure():
    def __init__(self, value, unit):
        if not isinstance(unit, Unit):
            raise TypeError("unit passed to Measure must be of type Unit!")
        self.unit = unit
        if isinstance(value, Measure): # TODO: Check that units are of the same dimensions
            if not value.unit.value[2] == self.unit.value[2]:
                raise TypeError("Measurement passed is not of the same unit type!")
            self.value = float(round(value.value * value.unit.value[0] / self.unit.value[0], 1))
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
        if isinstance(rhs, (int, float)):
            return False
        elif isinstance(rhs, Measure):
            c = Measure(rhs, self.unit)
            return self.value == c.value
    
    def __gt__(self, rhs):
        if isinstance(rhs, (int, float)):
            c = float(rhs)
            return self.value > c
        elif isinstance(rhs, Measure):
            c = Measure(rhs, self.unit)
            return self.value > c.value

    def __lt__(self, rhs):
        if isinstance(rhs, (int, float)):
            c = float(rhs)
            return self.value < rhs
        elif isinstance(rhs, Measure):
            c = Measure(rhs, self.unit)
            return self.value < c.value

    def __mul__(self, rhs):
        com = Measure(rhs, self.unit)
        return Measure(com.value * self.value, self.unit)

    def __truediv__(self, rhs):
        com = Measure(rhs, self.unit)
        return Measure(self.value / com.value, self.unit)

    def __floordiv__(self, rhs):
        com = Measure(rhs, self.unit)
        return Measure(self.value // com.value, self.unit)

    def __sub__(self, rhs):
        com = Measure(rhs, self.unit)
        return Measure(self.value - com.value, self.unit)

    def __add__(self, rhs):
        com = Measure(rhs, self.unit)
        return Measure(self.value + com.value, self.unit)

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

    @staticmethod
    def parse_measure(string, unit_string=None): # TODO: This needs finished, currently only works if you supply the unit_string
        if unit_string:
            if unit_string in MassUnit.get_abbreviation_list():
                unit = MassUnit.get_unit_from_abbreviation(unit_string)
            elif unit_string in LengthUnit.get_abbreviation_list():
                unit = LengthUnit.get_unit_from_abbreviation(unit_string)

            try:
                if isinstance(string, str):
                    value = float(string)
                elif isinstance(string, int):
                    value = float(string)
                elif isinstance(string, float):
                    value = string

            except ValueError:
                raise ValueError("String passed to parse_measure is not a number!")
            if isinstance(unit, MassUnit):
                return MassMeasure(value, unit)
            elif isinstance(unit, LengthUnit):
                return LengthMeasure(value, unit)

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
        super().__init__(measure, VolumentUnit.MILLILITER)

class Liters(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.LITER)

class Cups(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumentUnit.CUP)

class Pints(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.PINT)

class Quarts(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumentUnit.QUART)

class Gallons(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.GALLON)

class Tablespoons(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumentUnit.TABLESPOON)

class Teaspoons(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.TEASPOON)

class FluidOunces(VolumeMeasure):
    def __init__(self, measure):
        super().__init__(measure, VolumeUnit.FLUID_OUNCE)
