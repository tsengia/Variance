# Variance

Variance is a Python 3 tool to autogenerate weightlifting programs and meal plans.

This is by no means a complete tool, or built by any medical/fitness professional.
This is basically a side project for me to learn more about weightlifting while also contributing to open source, and also hopefully creating a time saver in the future for myself and others.


# Installation
`pip install -r requirements.txt`

TODO: Write instructions for setting up `.env` file, provide a sample `.env` file. Provide a script for starting the server.

## Bootstrapping
Bootstrapping Variance means initializing the database, filling it with default values, and loading any static assets.
To initialize the database:
`flask init-db`
To add in the default units:
`flask add-default-units`


# Developing
First, `git clone` the repo and `cd` into it.  
Next, create a virtual environment: `python3 -m venv env`   
Then activate the virtual environment: `./env/Scripts/activate`  
Now install the dependencies: `pip install -r requirements_dev.txt`  

Next, load in the default data using the following commands:  
`flask load-fixture units`  
`flask load-fixture muscles`  
`flask load-fixture equipment`  
`flask load-fixture gym`  
`flask load-fixture exercises`  

# Testing
Because Variance is a flask web API, it uses both unit testing and functional testing to verify that it works.  
To run the test suite, `cd` into the toplevel directory and run:  
`python -m pytest`  

All tests are stored in the `tests/` directory. Unit tests are in `tests/unit/` and functional tests are in `tests/functional/`.
