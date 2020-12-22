from util import nutritionlabel

class Recipie():

    def __init__(self, name):
        self.name = name
        self.id = None
        self.ingredients = []
        self.additions = []
        self.instructions = ""
        self.nutrition = nutritionlabel()
        self.macrotypes = []
        self.time = 0
