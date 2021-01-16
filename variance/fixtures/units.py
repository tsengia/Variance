
# Format of the below tuples:
# (multiplier ("abbreviation", ..., "plural-name"), "dimension")

DEFAULT_UNITS = [
# Mass
(1,("g", "gram", "grams"), "mass"),
(453.5924,("lb", "lbs", "pound", "pounds"),"mass"),
(28.34952,("oz", "ounce", "ounces"),"mass"),
(1000,("kg", "kilogram", "kilograms"),"mass"),
(0.001, ("mg", "milligram", "milligrams"),"mass"),
(6350.293, ("st", "stone"), "mass"),
# Length
(1,("m", "meter", "meters"),"length"),
(0.01,("cm", "centimeter", "centimeters"),"length"),
(0.3048,("ft", "foot", "feet"),"length"),
(0.0254,("in", "inch", "inches"),"length"),
(0.9144,("yd", "yard", "yards"),"length"),
(1000,("km", "kilometer", "kilometers"),"length"),
(1609.344,("mi", "mile", "miles"),"length"),
# Energy
(1,("Cal", "kcal", "kilocalorie","kilocalories","Calorie","Calories"), "energy"), # NOTE: This is Food Calories. So 1 Cal == 1000calories
(0.00023900573614,("J", "jewel", "jewels"),"energy"),
# Volume
(1,("mL", "ml", "milli-liter", "milli-liters", "milliliter", "milliliters"),"volume"),
(1000, ("L", "liter", "liters"),"volume"),
(240, ("cup", "cups"), "volume"),
(960, ("qt", "quart", "quarts"), "volume"),
(3840, ("gal", "Gal", "gallon", "gallons"), "volume"),
(480, ("pt", "pint", "pints"), "volume"), # 2 cups
(120, ("gill", "gills"), "volume"), # I swear if I ever have to use this unit... tally of times unit is used: 0
(30, ("fl oz", "fl. oz.", "fl-oz", "fl. oz", "fluid ounce", "fluid ounces"), "volume"), # 1/8 of a cup
(15, ("tbsp", "tablespoon", "tablespoons"), "volume"),  # 1/16 of a cup
(5, ("tsp", "teaspoon", "teaspoons"), "volume"), # 1/48 of a cup
# Time
(1,("s", "sec","second","seconds"), "time"),
(60,("min", "minute", "minutes"),"time"),
(3600,("hr", "hour", "hours"), "time"),
# Speed
(1,("m/s", "meters per second","meters/second"), "speed"),
(0.44704,("mph", "miles per hour", "miles/hour"),"speed"),
(0.2777778,("kmph", "kilometers per hour", "kilometers/hour"), "speed")
]