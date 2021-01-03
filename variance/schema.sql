DROP TABLE IF EXISTS UserIndex;
DROP TABLE IF EXISTS EquipmentIndex;
DROP TABLE IF EXISTS ExerciseIndex;
DROP TABLE IF EXISTS ExerciseLogs;
DROP TABLE IF EXISTS ConsumableIndex;
DROP TABLE IF EXISTS RecipieIndex;
DROP TABLE IF EXISTS IngredientIndex;
DROP TABLE IF EXISTS TrackerIndex;
DROP TABLE IF EXISTS TrackerLogs;
DROP TABLE IF EXISTS UnitIndex;
DROP TABLE IF EXISTS MuscleIndex;
DROP TABLE IF EXISTS ExerciseMuscles;
DROP TABLE IF EXISTS MicronutrientIndex;
DROP TABLE IF EXISTS IngredientMicronutrients;
DROP TABLE IF EXISTS ConsumableMicronutrients;
DROP TABLE IF EXISTS RecipieMicronutrients;
DROP TABLE IF EXISTS RecipieIngredients;
DROP TABLE IF EXISTS ProgramIndex;
DROP TABLE IF EXISTS ProgramDays;
DROP TABLE IF EXISTS WorkoutIndex;
DROP TABLE IF EXISTS WorkoutExercises;

--List of users.
CREATE TABLE UserIndex(
	id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(20) UNIQUE NOT NULL, -- public username
	password TEXT NOT NULL, -- user password hash, includes method and salt
	email VARCHAR(50), -- private email address
	birthdate DATE NOT NULL, -- birthdate, used to calculate age
	created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- datetime that this account was created
	role INTEGER NOT NULL DEFAULT (0) -- 0=user, 1=trainer, 2=admin
);

--Stores a list of all the different types of trackers (default and user created) that exist.
--A tracker created by a user is public to all.
CREATE TABLE TrackerIndex(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE, -- Display name of this tracker
	dimension VARCHAR(30) NOT NULL, -- What does this tracker measure? Values: mass, volume, length, time, speed, energy, quantity
	removable BOOLEAN DEFAULT (1) -- If set to 1, the user may delete this tracker (some things, such as weight, won't be deleted)
);

--List of units. These may be default units or user made units.
CREATE TABLE UnitIndex(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(30) UNIQUE NOT NULL, -- Long form of this unit. Ex: "meters", "pounds"
	dimension VARCHAR(30) NOT NULL, -- What does this unit measure? Values: mass, volume, length, time, speed, energy, quantity
	abbreviation VARCHAR(20) NOT NULL -- Short form of this unit. Ex: "m", "lbs"
);

--List of equipment
CREATE TABLE EquipmentIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	description VARCHAR(230)
);

--List of muscles
CREATE TABLE MuscleIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL
);

--List of exercises
CREATE TABLE ExerciseIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	equipment INTEGER NOT NULL, -- Equipment required for this workout
	description TEXT,       
	FOREIGN KEY(equipment) REFERENCES EquipmentIndex(id)
);

--Junction table associating exercises with the muscles they work
CREATE TABLE ExerciseMuscles (
	exerciseID INTEGER NOT NULL,
	muscleID INTEGER NOT NULL,
       	FOREIGN KEY(exerciseID) REFERENCES ExerciseIndex(id),
       	FOREIGN KEY(muscleID) REFERENCES MuscleIndex(id),
	CONSTRAINT PK_ExerciseMuscles PRIMARY KEY (exerciseID, muscleID)
);

--Stores all exercise logs (1 log = 1 set) for ALL users. Each activity logs does not need to have a weight, duration, or repetition count. Activity logs can have any combination of those measures
--Set number allows multiple logs to be grouped together into one set (ie for a super set or a circuit)
--Set order dictates when the log was completed within the set number (0 means first, 1 = second, 2 = third)
CREATE TABLE ExerciseLogs (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	userID INTEGER NOT NULL, -- What user entered this log?
	exerciseID INTEGER NOT NULL, -- What exercise did the user complete?
	time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- What time did the user enter this log?
	-- Below are the measures for the exercise log. Logs may have any combination of duration, weight and repetitions
	duration_value DECIMAL(5, 3),
	duration_unit INTEGER,
	weight_value DECIMAL(5, 3),
	weight_unit INTEGER,
	repetitions SMALLINT UNSIGNED,

	reps_in_reserve DECIMAL(2,1), -- Optional reps in reserve for measuring the intensity of this set
       	-- Constraints/foreign keys
	FOREIGN KEY(userID) REFERENCES UserIndex(id),
       	FOREIGN KEY(exerciseID) REFERENCES ExcerciseIndex(id),
       	FOREIGN KEY(duration_unit) REFERENCES UnitIndex(id),
       	FOREIGN KEY(weight_unit) REFERENCES UnitIndex(id)
);

--Stores all the logs for all the trackers
CREATE TABLE TrackerLogs (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	userID INTEGER NOT NULL, -- What user does this log belong to?
	time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- What time was this log measured?
	value DECIMAL(7, 4) NOT NULL, -- What is the value of this measure?
	unit INTEGER NOT NULL, -- What unit was this measurement in?
	FOREIGN KEY(userID) REFERENCES UserIndex(id),
       	FOREIGN KEY(unit) REFERENCES UnitIndex(id)
);

--List of all fitness programs
CREATE TABLE ProgramIndex(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	author INTEGER NOT NULL, -- UserID of the who created this program
	public BOOLEAN NOT NULL DEFAULT(0), -- If set to 1, all users can see this program
	description TEXT,
	duration SMALLINT NOT NULL DEFAULT (1), -- How many different days are within this program?
	FOREIGN KEY(author) REFERENCES UserIndex(id)
);

--List of all the days in each program
CREATE TABLE ProgramDays(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	program INTEGER NOT NULL, -- What program does this day belong to?
	name VARCHAR(50) NOT NULL, -- What is the name of this day? Ex: "Monday Upperbody", "Lowerbody 2"
	workout_count TINYINT NOT NULL DEFAULT(1), -- How many times will the user workout on this day? Default is just once a day.
	FOREIGN KEY(workout_count) REFERENCES ProgramIndex(id)
);

--List of all workouts
CREATE TABLE WorkoutIndex(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	program_day INTEGER NOT NULL, -- What program_day does this belong to?
	workout_number TINYINT UNSIGNED NOT NULL DEFAULT(1), -- Is this the first or second workout of the day?
	name VARCHAR(50) NOT NULL, -- Name of this workout Ex: "Morning Upperbody", "Squat Workout"
	FOREIGN KEY(program_day) REFERENCES ProgramDays(id)
);

--List of each exercise associated with each workout
CREATE TABLE WorkoutExercises(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	workout INTEGER NOT NULL,
	exercise INTEGER NOT NULL,
	
	-- Static target measures
	-- Target measures for this exercise, any combination of repetitions, weight, time, distance
	weight_value DECIMAL(5,3), -- Target weight for this set
	weight_unit INTEGER, -- Pounds? Kilograms?
	duration_value DECIMAL(5,3), -- Target duration for this set
	duration_unit INTEGER, -- Hours? Minutes? Seconds?
	repetitions SMALLINT UNSIGNED, -- Target number of repetitions for this set
	
	-- Relative target measures
	-- Optional: Calculate weight and/or duration based upon recent maximum values of an exercise
	relative_weight_percentage TINYINT UNSIGNED,
	relative_weight_exercise INTEGER,
	relative_duration_percentage TINYINT UNSIGNED,
	relative_duration_exercise INTEGER,
	
	--Intensity measures
	reps_in_reserve DECIMAL(2,1), -- Optional: Reps in reserve
	until_fail BOOLEAN NOT NULL DEFAULT(0), -- if set to 1, indicates that this exercise should be performed until exhaustion/failure
	
	--Super sets
	super_set_group TINYINT UNSIGNED, -- Optional: Exercises in the same super set should have the same super_set_group number

	--Constraints
	FOREIGN KEY(workout) REFERENCES WorkoutIndex(id),
	FOREIGN KEY(exercise) REFERENCES ExerciseIndex(id)
);

--List of micronutrients
CREATE TABLE MicronutrientIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(50)
);

--List of ingredients used to calculate nutritional value of recipies
CREATE TABLE IngredientIndex (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(50),
	serving_value DECIMAL(5,4),
	serving_unit INTEGER NOT NULL,
	calories INTEGER NOT NULL,
	protein INTEGER NOT NULL,
	fats INTEGER NOT NULL,
       	FOREIGN KEY(serving_unit) REFERENCES UnitIndex(id)
);

--Lists all recipies. Macros + calories are calculated at the time of recipie creation. Category should be treated as an enum.
--Current category enum values: 0 - entree, 1 - side, 2 - snack, 3 - dessert, 4 - drink
--macros are measured in grams per serving
CREATE TABLE RecipieIndex (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(59),
	serving_value DECIMAL(4,2) NOT NULL,
	serving_unit INTEGER NOT NULL,
	calories INTEGER NOT NULL,
	protein INTEGER NOT NULL,
	carbohydrates INTEGER NOT NULL,
	fats INTEGER NOT NULL,
	category TINYINT UNSIGNED,
	glycemic_index DECIMAL(2, 1),
	instructions TEXT,
	FOREIGN KEY(serving_unit) REFERENCES UnitIndex(id)
);

--Associates each recipie with the ingredients it contains and how much of that ingredient it uses.
CREATE TABLE RecipieIngredients (
	recipieID INTEGER NOT NULL,
	ingredientID INTEGER NOT NULL,
	measure_value DECIMAL(5,2) NOT NULL,
	measure_unit INTEGER NOT NULL,
       	FOREIGN KEY(recipieID) REFERENCES RecipieIndex(id),
       	FOREIGN KEY(ingredientID) REFERENCES IngredientIndex(id),
       	FOREIGN KEY(measure_unit) REFERENCES UnitIndex(id),
	CONSTRAINT PK_RecipieIngredients PRIMARY KEY(recipieID, ingredientID)
);

--List of generic consumables
CREATE TABLE ConsumableIndex (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(50),
	serving_value DECIMAL(5,2) NOT NULL,
	serving_unit INTEGER NOT NULL,
	calories INTEGER NOT NULL,
	protein INTEGER NOT NULL,
	carbohydrates INTEGER NOT NULL,
	fats INTEGER NOT NULL,
	glycemic_index DECIMAL(2,1),
       	FOREIGN KEY(serving_unit) REFERENCES UnitIndex(id)
);

--Associates ingredients with the micronutrients they contain (and how much in each serving)
CREATE TABLE IngredientMicronutrients (
	ingredientID INTEGER NOT NULL,
	micronutrientID INTEGER NOT NULL,
	measure_value DECIMAL(5,3) NOT NULL,
	measure_unit INTEGER NOT NULL,
       	FOREIGN KEY(ingredientID) REFERENCES IngredientIndex(id),
       	FOREIGN KEY(micronutrientID) REFERENCES MicronutrientIndex(id),
       	FOREIGN KEY(measure_unit) REFERENCES UnitIndex(id),
	CONSTRAINT PK_IngredientMicronutrients PRIMARY KEY(ingredientID, micronutrientID)
);

--Associates consumables with the micronutrients they contain (and how much in each serving)
CREATE TABLE ConsumableMicronutrients (
	consumableID INTEGER NOT NULL,
	micronutrientID INTEGER NOT NULL,
	measure_value DECIMAL(5,3) NOT NULL,
	measure_unit INTEGER NOT NULL,
       	FOREIGN KEY(consumableID) REFERENCES ConsumableIndex(id),
       	FOREIGN KEY(micronutrientID) REFERENCES MicronutrientIndex(id),
       	FOREIGN KEY(measure_unit) REFERENCES UnitIndex(id),
	CONSTRAINT PK_ConsumableMicronutrients PRIMARY KEY(consumableID, micronutrientID)
);

--Associates recipies with the micronutrients they contain (and how much in each serving)
CREATE TABLE RecipieMicronutrients (
	recipieID INTEGER NOT NULL,
	micronutrientID INTEGER NOT NULL,
	measure_value DECIMAL(5,3) NOT NULL,
	measure_unit INTEGER NOT NULL,
       	FOREIGN KEY(recipieID) REFERENCES RecipieIndex(id),
       	FOREIGN KEY(micronutrientID) REFERENCES MicronutrientIndex(id),
       	FOREIGN KEY(measure_unit) REFERENCES UnitIndex(id),
	CONSTRAINT PK_RecipieMicronutrients PRIMARY KEY(recipieID, micronutrientID)
);

