DROP TABLE IF EXISTS UserIndex;
DROP TABLE IF EXISTS EquipmentIndex;
DROP TABLE IF EXISTS ExerciseIndex;
DROP TABLE IF EXISTS ActivityLogs;
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


--List of units. These may be default units or custom made.
--dimension is what this unit measures, and should be treated like an enum.
--Dimension enum values: 0 - unitless/count/quantity, 1 - mass, 2 - volume, 3 - length, 4 - time, 5 - speed
CREATE TABLE UnitIndex(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(30) UNIQUE NOT NULL,
	dimension TINYINT NOT NULL,
	abbreviation VARCHAR(3) NOT NULL
);

--List of users. Role is an enum. 0 = normal user, 1 = trainer, 2 = admin.
CREATE TABLE UserIndex(
	id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(20) UNIQUE NOT NULL,
	password TEXT NOT NULL,
	birthdate DATE NOT NULL,
	created DATETIME NOT NULL DEFAULT (NOW()),
	role INTEGER NOT NULL DEFAULT (0)
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
	equipment INTEGER NOT NULL,
	description TEXT,       
	FOREIGN KEY(equipment) REFERENCES EquipmentIndex(id)
);

--Junction table associating exercises with the muscles they work
CREATE TABLE ExerciseMuscles (
	exerciseID INTEGER NOT NULL,
	muscleID INTEGER  NOT NULL,
       	FOREIGN KEY(exerciseID) REFERENCES ExerciseIndex(id),
       	FOREIGN KEY(muscleID) REFERENCES MuscleIndex(id),
	CONSTRAINT PK_ExerciseMuscles PRIMARY KEY (exerciseID, muscleID)
);

--Stores all activity logs (1 log = 1 set) for ALL users. Each activity logs does not need to have a weight, duration, or repetition count. Activity logs can have any combination of those measures
CREATE TABLE ActivityLogs (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	userID INTEGER NOT NULL,
	exerciseID INTEGER NOT NULL,
	time DATETIME NOT NULL DEFAULT (NOW()),
	duration_value DECIMAL(5, 3),
	duration_unit INTEGER,
	weight_value DECIMAL(5, 3),
	weight_unit INTEGER,
	repetitions TINYINT,
	reps_in_reserve DECIMAL(2,1),
       	FOREIGN KEY(userID) REFERENCES UserIndex(id),
       	FOREIGN KEY(exerciseID) REFERENCES ExcerciseIndex(id),
       	FOREIGN KEY(duration_unit) REFERENCES UnitIndex(id),
       	FOREIGN KEY(weight_unit) REFERENCES UnitIndex(id)
);

--Stores a list of all the different types of trackers (default and user created) that exist.
--If removable is set to 1 (true), then the user can delete this tracker from their account
CREATE TABLE TrackerIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	dimension TINYINT NOT NULL,
	removable BOOLEAN DEFAULT (1)
);

--Stores all the logs for all the trackers
CREATE TABLE TrackerLogs (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	time DATETIME NOT NULL DEFAULT (NOW()),
	value DECIMAL(7, 4) NOT NULL,
	unit INTEGER NOT NULL,
       	FOREIGN KEY(unit) REFERENCES UnitIndex(id)
);

--List of micronutrients
CREATE TABLE MicronutrientIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(50)
);

--List of ingredients used to calculate nutritional value of recipies
CREATE TABLE IngredientIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(59),
	serving_value DECIMAL(4,2) NOT NULL,
	serving_unit INTEGER NOT NULL,
	calories INTEGER NOT NULL,
	protein INTEGER NOT NULL,
	carbohydrates INTEGER NOT NULL,
	fats INTEGER NOT NULL,
	category TINYINT,
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
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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

