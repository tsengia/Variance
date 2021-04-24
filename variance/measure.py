import re
from models import UnitModel

class Measure():
    def __init__(self, value, unit, accuracy=6):
        if not isinstance(unit, UnitModel):
            raise TypeError("unit passed to Measure must be of type UnitModel!")
        self.unit = unit
        if isinstance(value, Measure): # TODO: Check that units are of the same dimensions
            if not value.unit.dimension == self.unit.dimension:
                raise TypeError("Measurement passed is not of the same unit dimension!")
            self.value = float(round(value.value * value.unit.multiplier / self.unit.multiplier, accuracy))
        elif isinstance(value, (int, float)):
            self.value = float(value)
        else:
            raise TypeError("value passed to Measure must be int, float, or Measure type!")

    def __str__(self):
        return str(self.value) + " " + str(self.unit.abbreviation)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __eq__(self, rhs):
        if isinstance(rhs, Measure):
            # Check to make sure they measure the same thing (both are length, or mass or volume, etc.)
            if not rhs.unit.dimension == self.unit.dimension:
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

class UnitParser():
    @staticmethod
    def parse(text):
        text = text.strip().lower().replace(".", "")

        abbreviation_match = UnitModel.query.filter_by(abbreviation=text).first()
        if abbreviation_match:
            return abbreviation_match

        name_match = UnitModel.query.filter_by(name=text).first()
        if name_match:
            return name_match

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