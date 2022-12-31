# Variance

Variance is a Python 3 tool to autogenerate weightlifting programs and meal plans.

This is by no means a complete tool, or built by any medical/fitness professional.
This is basically a side project for me to learn more about weightlifting while also contributing to open source, and also hopefully creating a time saver in the future for myself and others.

# Installation
`pip install -r requirements.txt`

# Starting the server
To start the flask webserver, set the `FLASK_APP` environmental variable to `variance.create_app` and then run `flask run`.

You will then be able to access the API by going to `http://localhost:5000/api`.

You can also access the Rapid API Doc by visiting: `http://localhost:5000/rapidoc`

## Bootstrapping
Bootstrapping Variance means initializing the database, filling it with default values, and loading any static assets.
To initialize the database:
```flask init-db```  

To add in built-in units, equipment, muscles, exercises, etc., run this command:  
```flask all import variance/fixtures```

# Developing
First, `git clone` the repo and `cd` into it.  
Next, create a virtual environment: `python3 -m venv env`   
Then activate the virtual environment: `./env/Scripts/activate`  
Now install the dependencies: `pip install -r requirements_dev.txt`  

# Testing
Because Variance is a flask web API, it uses both unit testing and functional testing to verify that it works.  

To run the test suite, `cd` into the toplevel directory and run:  
`python -m pytest`  

All tests are stored in the `tests/` directory.  
Unit tests are in `tests/unit/` and functional tests are in `tests/functional/`.

# Resource Types
Variance contains the following resources/models:
|Resource Name  |Handle           |Description|
|--------------:|:---------------:|:----------|
|Units          |`units`          |Measurement units to enable conversion between units and user-defined units|
|Muscles        |`muscles`        |Locations, descriptions, and diagrams of muscles|
|Muscle Groups  |`muscles groups` |Larger groups of muscles (ie. "upper-body" or "legs")|
|Equipment      |`equipment`      |Description of equipment used during exercise|
|Exercise       |`exercises`      |Exercise description|
|Gym            |`gyms`           |Collections of Equipment and additional info|
|Nutrient Info  |`nutrients`      |Micro and macronutrient descriptions and info|
|Trackers       |`trackers`       |Personal goals, weight tracking|
|Consumables    |`consumables`    |Food, recipies, drinks and their nutritional content|
|Mealplans      |`mealplans`      |WIP|
|Workouts       |`workouts`       |WIP|

# Exporting Data
To export your data for backup or sharing, run the following command:
```
flask <resource_handle> export <export_root>
```

Where `<resource_handle>` is the [resource type](#resource-types) that you are exporting, and `<export_root>` is the location that the exported data will be stored under.

Example:
```
flask exercises export my-export
```


# Importing Data
To import data from a previously created data export, run the following command:
```
flask <resource_handle> import <import_root>
```

Where `<resource_handle>` is the [resource type](#resource-types) that you are importing, and `<import_root>` is the location of the exported root directory.

Example:
```
flask exercises import my-export/
```