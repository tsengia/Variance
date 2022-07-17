# List of default exercises
DEFAULT_EXERCISES=[
# Name, Description, Measurement

# Bench Press
("Bench Press", "Flat bench press using a barbell.", "weight"), # 1
("DB Bench Press", "Flat bench press using dumbbells.", "weight"),
("Incline Bench Press", "Inclined bench press using a barbell.", "weight"),
("Incline DB Bench Press", "Inclined bench press using a dumbbell.", "weight"),
("Decline Bench Press", "Declined bench press using a barbell", "weight"),
("Decline DB Bench Press", "Declined bench press using dumbbells", "weight"),
("Narrow Grip Bench Press", "Flat bench press using a barbell, hands placed shoulder width apart.", "weight"),

# Squat
("Back Squat", "Traditional back squat with a barbell", "weight"), # 8
("Front Squat", "Front squat using a barbell.", "weight"),
("Goblet Squat", "Front squat using a sinngle barbell.", "weight"),
("Pause Squat", "Back squat with a barbell, but a pause in movement at the bottom of the motion", "weight"),
("DB Split Squat", "One legged squats with DBs as weight. Also called bulgarian split squats.", "weight"),

# Overhead Press/Military Press
("Standing Overhead Press", "Overhead press with a barbell while standing.", "weight"), # 12
("Seated Overhead Press", "Overhead press with a barbell while sitting.", "weight"),
("Standing DB Overhead Press", "Overhead press with dumbbells while standing.", "weight"),
("Seated DB Overhead Press", "Overhead press with dumbbells while sitting.", "weight"),

# Rows & Back
("Seated Cable Rows", "Seated rows using a rowing machine.", "weight"),
("Seated One-Arm Cable Rows", "Seated one-arm rows using a rowing machine.", "weight"),
("Bent Over Row", "Standing, bent over rows using a barbell.", "weight"),
("DB Bent Over Row", "Single arm bent over rows using a barbell.", "weight"),
("Barbell Shrugs", "Standing barbell shrugs.", "weight"),
("Seated Overhead Cable Pulldown", "Lat pull downs.", "weight"),

# Arm Curls
("Barbell Curl", "Standing bicep curl using a barbell.", "weight"),
("DB Curl", "Standing bicep curl using dumbbells.", "weight"),
("Wrist Curl", "Single forearm curls using a dumbbell.", "weight"),
### TO ADD: Preacher curls? Cable curls?

# Bodyweight
("Pull Ups", "Pull Up.", "reps"),
("Weighted Pull Ups", "Pull up with additional weight attached.", "weight"),
("Push Ups", "Push up.", "reps"),
("Weighted Push Ups", "Push up with additional weight on top.", "weight"),
("Dips", "Dips.", "reps"),
("Weighted Dips", "Dips with additional weight on top.", "weight"),
("Box Jumps", "Box jumps", "reps"),

# Cleans/Pulls
("Power Clean", "Barbell power clean.", "weight"),
("Hang Clean", "Barbell hang clean.", "weight"),
("Clean and Jerk", "Barbell clean and jerk.", "weight"),
("Snatch", "Barbell snatch.", "weight"),
("Deadlift", "Barbell deadlift", "weight"),

# Triceps
("Cable Tricep Pushdowns", "Tricep pushdown using a cable machine.", "weight"),
("Lying Tricep Extension", "Tricep extension done overhead while lying down.", "weight"),

# Misc. Legs
("Leg Curls", "Seated leg curls using a leg curl machine.", "weight"),
("Leg Extension", "Seated leg extension using a leg extension machine.", "weight"),
("DB Lunges", "Weighted lunges.", "weight"),
("Toe Raises", "Weighted toe raises.", "weight"),

# Misc.
("DB Lateral Side Raises", "Standing side raises with DBs, also called 'pouring milk'.", "weight"),
("DB Front Raises", "Standing front raises with DBs", "weight")

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
