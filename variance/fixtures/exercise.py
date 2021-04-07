# List of default exercises
DEFAULT_EXERCISES=[
# Name, Description, Measurement, list of equipment ID, parent exercise ID

# Bench Press
("Bench Press", "Flat bench press using a barbell.", "weight", [2,7], None), # 1
("DB Bench Press", "Flat bench press using dumbbells.", "weight", [1,7], 1),
("Incline Bench Press", "Inclined bench press using a barbell.", "weight", [2,8], 1),
("Incline DB Bench Press", "Inclined bench press using a dumbbell.", "weight", [1,8], 1),
("Decline Bench Press", "Declined bench press using a barbell", "weight", [2,9], 1),
("Decline DB Bench Press", "Declined bench press using dumbbells", "weight", [1,9], 1),
("Narrow Grip Bench Press", "Flat bench press using a barbell, hands placed shoulder width apart.", "weight", [2,7], 1),

# Squat
("Back Squat", "Traditional back squat with a barbell", "weight", [2,3], None), # 8
("Front Squat", "Front squat using a barbell.", "weight", [2,3], 8),
("Goblet Squat", "Front squat using a sinngle barbell.", "weight", [1], 8),
("Pause Squat", "Back squat with a barbell, but a pause in movement at the bottom of the motion", "weight", [2,3], 8),

# Overhead Press
("Standing Overhead Press", "Overhead press with a barbell while standing.", "weight", [2], None), # 12
("Seated Overhead Press", "Overhead press with a barbell while sitting.", "weight", [2], 12),
("Standing DB Overhead Press", "Overhead press with dumbbells while standing.", "weight", [1], 12),
("Seated DB Overhead Press", "Overhead press with dumbbells while sitting.", "weight", [1], 12),

# Rows
("Seated Cable Rows", "Seated rows using a rowing machine.", "weight", [12], None), # 16
("Bent Over Row", "Standing, bent over rows using a barbell.", "weight", [2], None), # 17
("DB Bent Over Row", "Single arm bent over rows using a barbell.", "weight", [1,7], 17),

# Curls
("Barbell Curl", "Standing bicep curl using a barbell.", "weight", [2], None),
("DB Curl", "Standing bicep curl using dumbbells.", "weight", [1], None),

# Bodyweight
("Pull Ups", "Pull Up.", "reps", [6], None),
("Weighted Pull Ups", "Pull up with additional weight attached.", "weight", None, None),
("Push Ups", "Push up.", "reps", None, None),
("Weighted Push Ups", "Push up with additional weight on top.", "weight", None, None),

]

# Naming convention for exercises:
# [grip-variation] [body-posture-variation] [DB | Cable | Lever | Weighted | Assisted] <root motion name>
# DB is short for Dumbbells. If it lacks DB and is weighted, assume barbell.
# The "Cable" modifier is used to denote that the exercise is performed with some form of cabled machine.
# The "Lever" modifier is used to denote that the exercise is performed with some form of leverage machine
# The "Weighted" modifier is used for bodyweight exercises that use additional weight (chains, plates, medicine balls, etc.)
# The "Assisted" modifier is used for bodyweight exercises that use equipment or human assistance to complete the exercise (bands, cables, etc.)
# grip-variation = Wide, Medium, Narrow (biacromial - armpit to armpit distance)
# body-posture-variation = Flat, Upright (90 degrees), Incline, Decline, Seated, Standing
# This is not an exhaustive convention, however it is enough for a preliminary collection of exercises.