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

# Unit Testing
There are two "sections" of Variance, an API, and a small Python library for a future GUI (I call this the "core" library, it's stored in `variance/core/`).
To test the RESTful API, run:  
`python3.7 -m unittest discover -s test/api/`  

To test the core library, run:  
`python3.7 -m unitttest discover -s test/core/`
