DROP TABLE IF EXISTS UserIndex;
DROP TABLE IF EXISTS EquipmentIndex;
DROP TABLE IF EXISTS ActivityIndex;
DROP TABLE IF EXISTS ConsumableIndex;
DROP TABLE IF EXISTS RecipieIndex;
DROP TABLE IF EXISTS IngredientIndex;
DROP TABLE IF EXISTS TrackerIndex;

--List of units. These may be default units or custom made.
--dimension is what this unit measures, and should be treated like an enum.
--Dimension enum values: 0 - unitless/count/quantity, 1 - mass, 2 - volume, 3 - length, 4 - time, 5 - speed
CREATE TABLE UnitIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(30) NOT NULL UNIQUE,
	dimension TINYINT NOT NULL,
	abbreviation VARCHAR(3) NOT NULL
);

--List of users. Role is an enum. 0 = normal user, 1 = trainer, 2 = admin.
CREATE TABLE UserIndex (
	id INTEGER UNIQUE NOT_NULL PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(20) UNIQUE NOT_NULL,
	password TEXT NOT_NULL,
	birthdate DATE NOT_NULL,
	created DATETIME NOT_NULL DEFAULT NOW(),
	role INTEGER NOT_NULL DEFAULT 0,
);

--List of equipment
CREATE TABLE EquipmentIndex (
	id INTEGER NOT_NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT_NULL,
	description VARCHAR(230)
);

--List of muscles
CREATE TABLE MuscleIndex (
	id INTEGER NOT_NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT_NULL
);

--List of exercises
CREATE TABLE ExerciseIndex (
	id INTEGER NOT_NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT_NULL,
	equipment INTEGER NOT NULL FOREIGN KEY REFERENCES EquipmentIndex(id),
	description TEXT
);

--Junction table associating exercises with the muscles they work
CREATE TABLE ExerciseMuscle (
	exerciseID INTEGER NOT NULL FOREIGN KEY REFERENCES ExerciseIndex(id),
	muscleID INTEGER  NOT NULL FOREIGN KEY REFERENCES MuscleIndex(id),
	CONSTRAINT PK_ExerciseMuscle PRIMARY KEY (exerciseID, muscleID)
);

--Stores all activity logs (1 log = 1 set) for ALL users. Each activity logs does not need to have a weight, duration, or repetition count. Activity logs can have any combination of those measures
CREATE TABLE ActivityLogs (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	userID INTEGER NOT NULL FOREIGN KEY REFERENCES UserIndex(id),
	exerciseID INTEGER NOT NULL FOREIGN KEY REFERENCES ExcerciseIndex(id),
	time DATETIME NOT NULL DEFAULT NOW()
	duration_value DECIMAL(5, 3),
	duration_unit INTEGER FOREIGN KEY REFERENCES UnitIndex(id),
	weight_value DECIMAL(5, 3),
	weight_unit INTEGER FOREIGN KEY REFERENCES UnitIndex(id),
	repetitions TINYINT,
	reps_in_reserve DECIMAL(2,1)
);

--Stores a list of all the different types of trackers (default and user created) that exist.
--If removable is set to 1 (true), then the user can delete this tracker from their account
CREATE TABLE TrackerIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	dimension TINYINT NOT NULL,
	removable BOOLEAN DEFAULT 1
);

--Stores all the logs for all the trackers
CREATE TABLE TrackerLogs (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	time DATETIME NOT NULL DEFAULT NOW(),
	value DECIMAL(7, 4) NOT NULL,
	unit INTEGER NOT NULL FOREIGN KEY REFERENCES UnitIndex(id)
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
	serving_unit INTEGER NOT NULL FOREIGN KEY REFERENCES UnitIndex(id)
	calories INTEGER NOT NULL,
	protein INTEGER NOT NULL,
	fats INTEGER NOT NULL
);

--Lists all recipies. Macros + calories are calculated at the time of recipie creation. Category should be treated as an enum.
--Current category enum values: 0 - entree, 1 - side, 2 - snack, 3 - dessert, 4 - drink
--macros are measured in grams per serving
CREATE TABLE RecipieIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(59),
	serving_value DECIMAL(4,2) NOT NULL,
	serving_unit INTEGER NOT NULL FOREIGN KEY REFERENCES UnitIndex(id),
	calories INTEGER NOT NULL,
	protein INTEGER NOT NULL,
	carbohydrates INTEGER NOT NULL,
	fats INTEGER NOT NULL,
	category TINYINT,
	glycemic_index DECIMAL(2, 1),
	instructions TEXT
);

--Associates each recipie with the ingredients it contains and how much of that ingredient it uses.
CREATE TABLE RecipieIngredients (
	recipieID INTEGER NOT NULL FOREIGN KEY REFERENCES RecipieIndex(id),
	ingredientID INTEGER NOT NULL FOREIGN KEY REFERENCES IngredientIndex(id),
	measure_value DECIMAL(5,2) NOT NULL,
	measure_unit INTEGER NOT NULL FOREIGN KEY REFERENCES UnitIndex(id),
	CONSTRAINT PK_RecipieIngredients PRIMARY KEY(recipieID, ingredientID)
);

--List of generic consumables
CREATE TABLE ConsumableIndex (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(50),
	serving_value DECIMAL(5,2) NOT NULL,
	serving_unit INTEGER NOT NULL FOREIGN KEY REFERENCES UnitIndex(id),
	calories INTEGER NOT NULL,
	protein INTEGER NOT NULL,
	carbohydrates INTEGER NOT NULL,
	fats INTEGER NOT NULL,
	glycemic_index DECIMAL(2,1)
);

--Associates ingredients with the micronutrients they contain (and how much in each serving)
CREATE TABLE IngredientMicronutrients (
	ingredientID INTEGER NOT NULL FOREIGN KEY REFERENCES IngredientIndex(id),
	micronutrientID INTEGER NOT NULL FOREIGN KEY REFERENCES MicronutrientIndex(id),
	measure_value DECIMAL(5,3) NOT NULL,
	measure_unit INTEGER NOT NULL FOREIGN KEY REFERENCES UnitIndex(id),
	CONSTRAINT PK_IngredientMicronutrients PRIMARY KEY(ingredientID, micronutrientID)
);

--Associates consumables with the micronutrients they contain (and how much in each serving)
CREATE TABLE ConsumableMicronutrients (
	consumableID INTEGER NOT NULL FOREIGN KEY REFERENCES ConsumableIndex(id),
	micronutrientID INTEGER NOT NULL FOREIGN KEY REFERENCES MicronutrientIndex(id),
	measure_value DECIMAL(5,3) NOT NULL,
	measure_unit INTEGER NOT NULL FOREIGN KEY REFERENCES UnitIndex(id),
	CONSTRAINT PK_ConsumableMicronutrients PRIMARY KEY(consumableID, micronutrientID)
);

--Associates recipies with the micronutrients they contain (and how much in each serving)
CREATE TABLE RecipieMicronutrients (
	recipieID INTEGER NOT NULL FOREIGN KEY REFERENCES RecipieIndex(id),
	micronutrientID INTEGER NOT NULL FOREIGN KEY REFERENCES MicronutrientIndex(id),
	measure_value DECIMAL(5,3) NOT NULL,
	measure_unit INTEGER NOT NULL FOREIGN KEY REFERENCES UnitIndex(id),
	CONSTRAINT PK_RecipieMicronutrients PRIMARY KEY(recipieID, micronutrientID)
);

