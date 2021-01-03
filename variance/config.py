from os import path
from os import environ as e
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config():
    SECRET_KEY = e.load("SECRET_KEY")
    SESSION_COOKIES_NAME = e.load("SESSION_COOKIE_NAME")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

class ProdConfig(Config):
    FLASK_ENV="production"
    DEBUG=False
    TESTING=False
    DATABASE_URI=e.get("PROD_DATABASE_URI")

class DevConfig(Config):
    FLASK_ENV="development"
    DEBUG=True
    TESTING=True
    DATABASE_URI=e.get("DEV_DATABASE_URI")

class UnitTestConfig(DevConfig):
    DATABASE_URI=e.get("UNIT_TEST_DATABASE_URI")
