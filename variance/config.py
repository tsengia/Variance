"""
Classes and functions for loading runtime configuration
"""

from os import path
from os import environ as e
from dotenv import load_dotenv

def load_config_env():
    "Reads in the environmental variables from ../.env file"
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, '../.env'))

class Config():
    "Base Config class"
    SESSION_COOKIES_NAME = e.get("SESSION_COOKIE_NAME")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = "VarianceAPI"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0"
    OPENAPI_JSON_PATH = "variance-openapi.json"

class ProdConfig(Config):
    "Configuration that uses the secret key from the .env file and production database URI"
    SECRET_KEY = e.get("SECRET_KEY")
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = e.get("PROD_DATABASE_URI")


class DevConfig(Config):
    "Configuration for development, do NOT use in product, insecure secret key."
    SECRET_KEY = "DEVELOPMENT KEY"
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = e.get("DEV_DATABASE_URI")
    SQLALCHEMY_ECHO = True
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

class UnitTestConfig(DevConfig):
    "Configuration for Unit Testing, should have in-memory SQLite DB"
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"
    SQLALCHEMY_ECHO = False
