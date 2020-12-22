from enum import Enum
from .units import *

class Sex(Enum):
    MALE = 0
    FEMALE = 1

    def __str__(self):
        if self == Sex.MALE:
            return "male"
        if self == Sex.FEMALE:
            return "female"

    __repr__ = __str__

# Stores data (measured and derived) about body composition and statistics
# Note: This does not calculate any body composition data. It only stores it and provides information based upon it, such as BMI, BMR, RDEE, lean muscle mass (% and weight). Calculating body composition is a difficult, and possibly inaccurate task that varies for each user. Some may use a tape measure, others skin calipers, others may use displacement methods.
class Body():
    # Mifflin St. Jeor basal metabolic rate equation
    def get_bmr(self):
        sex_modifier = -161
        if self.sex == Sex.MALE:
            sex_modifier = 5
        return Calories(float(Kilograms(self.weight)) + (6.25 * float(Centimeters(self.height))) - (5.0 * self.age) + sex_modifier)

    # Katch McArdle equation for Resting Daily Energy Expenditure
    def get_rdee(self):
        return Calories(370 + (21.6 * Kilograms(self.lean_muscle_mass)))

    def get_bmi(self):
        return float(Kilograms(self.weight)) / (float(Meters(self.height))**2)

    def get_ffmi(self): # Normalized ffmi
        return (float(Kilograms(self.fat_free_mass)) / (float(Meters(self.height))**2)) + (6.1*(1.8-Meters(self.height)))

    @property
    def rdee(self):
        return self.get_rdee()

    @property
    def bmr(self):
        return self.get_bmr()

    @property
    def ffmi(self):
        return self.get_ffmi()

    @property
    def bmi(self):
        return self.get_bmi()

    @property
    def fat_free_mass(self):
        return Kilograms(self.weight) * (1 - self.fat_percentage)

    @property
    def fat_mass(self):
        return self.weight * self.fat_percentage

    def get_fat_percentage_from_bmi(self):
        b = self.get_bmi()
        sex_modifier = 0
        if self.sex == Sex.MALE:
            sex_modifier = 1
        return ((1.39 * b) + (0.16 * self.age) - (10.34 * sex_modifier) - 9)/100

    def get_bmi_category(self):
        b = self.bmi
        if b <= 15:
            return "Very severely underweight"
        if b <= 16:
            return "Severely underweight"
        if b <= 18.5:
            return "Underweight"
        if b <= 25:
            return "Normal"
        if b <= 30:
            return "Overweight"
        if b <= 35:
            return "Obese Class I"
        if b <= 40:
            return "Obese Class II"
        if b > 40:
            return "Obese Class III"

    @staticmethod
    def from_bmi(user):
        return BodyComposition(user.sex, user.age, user.height, user.weight)

    def __init__(self, sex, age, height, weight, fat_percentage=None, method=None):
        self.sex = sex
        self.age = age
        self.height = height
        self.weight = weight
        if not fat_percentage:
            self.fat_percentage = self.get_fat_percentage_from_bmi()
            self.method = "bmi"
        else:
            self.fat_percentage = fat_percentage
            self.method = method

