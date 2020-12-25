from .units import *
from .nutrition import MacroList

class Consumable():
    def calories(self, serving_size):
        return self.macros.calories_from_macros(serving_size)

    def __init__(name):
        self.name = name
        self.macros = MacroList(0, 0, 0)
        self.micros = {}
