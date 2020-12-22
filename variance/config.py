from pathlib import Path
from .units import *

# API Key used to look up nutritional information, register
USDA_API_KEY="zTrrytuPIfz2OFw26C3rSlHJ4aHBZaGFPynPajUi"

#path to where user data will be stored
USER_PATH=Path("/home/rectangle/Documents/Programming/Projects/Variance/user")

# Preffered Units for features

# When generating food plans & instructions, what unit do you want?

FOOD_MASS_UNITS=MassUnit.OUNCE
#FOOD_MASS_UNITS=MassUnit.GRAM

# When generating workout plans, what unit do you want?
LIFTING_UNITS=MassUnit.POUND
#LIFTING_"UNITS=MassUnit.KILOGRAM

# When tracking & displaying bodyweight, what unit do you want?
WEIGHT_TRACK_UNITS=MassUnit.POUND
#WEIGHT_TRACK_UNITS=MassUnit.KILOGRAM

HEIGHT_TRACK_UNITS=LengthUnit.INCH
#HEIGHT_TRACK_UNITS=LengthUnit.CENTIMETER

# When tracking & displaying body sizes (height, neck width, waist, etc):
SIZE_TRACK_UNITS=LengthUnit.INCH
#SIZE_TRACK_UNITS=LengthUnit.CENTIMETER
