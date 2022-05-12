from os import path
from os import environ as e
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))


class Config():
    SESSION_COOKIES_NAME = e.get("SESSION_COOKIE_NAME")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = "VarianceAPI"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0"
    OPENAPI_JSON_PATH = "variance-openapi.json"

class ProdConfig(Config):
    SECRET_KEY = e.get("SECRET_KEY")
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = e.get("PROD_DATABASE_URI")


class DevConfig(Config):
    SECRET_KEY = "DEVELOPMENT KEY"
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = e.get("DEV_DATABASE_URI")
    SQLALCHEMY_ECHO = True


class UnitTestConfig(DevConfig):
    SQLALCHEMY_DATABASE_URI = e.get("UNIT_TEST_DATABASE_URI")
    SQLALCHEMY_ECHO = False
