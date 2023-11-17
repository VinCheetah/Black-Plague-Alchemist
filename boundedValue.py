from math import inf

class BoundedValue(object):
    def __init__(self, value, minimum=-inf, maximum=inf):
        self.value: type(value)
        self.min: float
        self.max: float
        self.__setattr__("min", minimum, check=False)
        self.__setattr__("max", maximum, check=False)
        self.__setattr__("value", value)
        self.check_extremum()

    def check(self):
        self.value = min(max(self.value, self.min), self.max)

    def check_extremum(self):
        if self.min > self.max:
            raise InvalidExtremum

    def set_extremum(self, new_min, new_max):
        self.min = new_min
        self.max = new_max
        self.check()

    def set_min(self, new_min):
        self.min = new_min
        self.check()

    def set_max(self, new_max):
        self.max = new_max
        self.check()

    def set_value(self, value):
        self.value = value

    def reduce_max(self, new_max):
        self.max = min(self.max, new_max)

    def increase_min(self, new_min):
        self.min = max(self.min, new_min)

    def closer_extremum(self, new_min, new_max):
        self.increase_min(new_min)
        self.reduce_max(new_max)

    def unbound(self):
        self.set_extremum(-inf, inf)

    def __setattr__(self, key, value, check=True):
        if key == "value":
            super().__setattr__(key, min(max(value, self.min), self.max))
        elif key in ["min", "max"]:
            super().__setattr__(key, float(value))
            if check:
                self.check()
        else:
            super().__setattr__(key, value)
        return self

    def __pos__(self):
        return self.value

    def __neg__(self):
        return -self.value

    def __abs__(self):
        return abs(self.value)

    def __invert__(self):
        return ~self.value

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __iadd__(self, other):
        self.value += other
        return self

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return other - self.value

    def __isub__(self, other):
        self.value -= other
        return self

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return other * self.value

    def __imul__(self, other):
        self.value *= other
        return self

    def __truediv__(self, other):
        return self.value / other

    def __rtruediv__(self, other):
        return other / self.value

    def __itruediv__(self, other):
        self.value /= other
        return self

    def __floordiv__(self, other):
        return self.value // other

    def __rfloordiv__(self, other):
        return other // self.value

    def __ifloordiv__(self, other):
        self.value //= other
        return self

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __str__(self):
        return f"{self.value}   (min : {self.min}, max : {self.max})"

    def __repr__(self):
        return str(self.value)


class InvalidExtremum(Exception):
    """Raised when extremes are not valid"""
    pass
