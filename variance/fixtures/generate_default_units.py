from variance.core.units import *

print("Generating add_default_units.sql....")
sql = open("add_default_units.sql", "w")
sql.write("INSERT INTO UnitIndex (name, abbreviation, dimension) VALUES\n")

sql.write("--Mass\n")
for u in MassUnit:
    sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

sql.write("--Volume\n")
for u in VolumeUnit:
    sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

sql.write("--Length\n")
for u in LengthUnit:
    sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

sql.write("--Energy\n")
for u in EnergyUnit:
    sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

sql.write("--Time\n")
for u in TimeUnit:
    sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

sql.write("--Speed\n")
for u in SpeedUnit:
    sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

sql.write("('deleted unit', 'del', 'deleted');")
sql.close()
print("add_default_units.sql generated.")
