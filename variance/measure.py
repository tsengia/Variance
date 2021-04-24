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