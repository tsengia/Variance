"""
Main entry point for Variance when running as a webserver
"""
import pathlib
import shutil
import logging
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api, Blueprint

from variance.extensions import db

def load_default_settings(app):
    from variance.api.defaults import DefaultSettingsManager
    instance_path = pathlib.Path(app.instance_path)
    defaults_path = instance_path / "defaults"
    app.defaults_manager = DefaultSettingsManager(defaults_path)
    logging.info("Default settings loaded.")

def setup_instance_path(instance_path):
    "Setup the instance directory structure"
    instance_path = pathlib.Path(instance_path)
    defaults_path = instance_path / "defaults"
    if not instance_path.exists():
        instance_path.mkdir(exist_ok=True)
        if not instance_path.is_dir():
            print("Instance directory could not be created! Exiting.")
            exit()
        defaults_path.mkdir(exist_ok=True)
        if not defaults_path.is_dir():
            print("Defaults settings directory could not be created! Exiting.")
            exit()
        shutil.copyfile(str(pathlib.Path("variance") / "defaults" / "user.json"), str(defaults_path / "user.json")) 
        logging.info("Created new instance directory")

def load_models(app):
    "Helper function that imports all the models"
    from variance.models import unit, muscle, equipment, exercise, gym, tracker, user, lambda_measure, permissions, workout, nutrition, mealplan
    logging.info("Variance Models imported.")

def load_cli(app):
    "Helper function that imports all the CLI commands"
    from variance import cli
    c = app.cli
    c.add_command(cli.db.db_cli)
    c.add_command(cli.permissions.permissions_cli)
    c.add_command(cli.user.user_cli)
    cli.equipment.equipment_cli.attach(c)
    cli.muscle.muscle_cli.attach(c)
    c.add_command(cli.gym.gym_cli)
    c.add_command(cli.exercise.exercise_cli)
    c.add_command(cli.unit.unit_cli)
    cli.nutrient.nutrient_cli.attach(c)
    c.add_command(cli.consumable.consumable_cli)
    c.add_command(cli.load_fixtures.lf_cli)

    logging.info("Variance CLI loaded.")

def load_api(rest_api):
    "Helper function that registers blueprints and versioning endpoints"
    version_bp = Blueprint("version", "version", url_prefix="/", description="Provides versioning information about the app.")

    @version_bp.route("/api/version")
    def api_verison():
        return {"apiversion": "0.1"}

    @version_bp.route("/version")
    def version():
        return {"version": "0.0.1 alpha"}
    
    from variance import api
    rest_api.register_blueprint(version_bp, url_prefix="/")
    rest_api.register_blueprint(api.auth.bp, url_prefix="/api/auth")
    rest_api.register_blueprint(api.units.bp, url_prefix="/api/units")

    logging.info("Variance API blueprints loaded.")

def create_app(test_config=None):
    "Main entry point, creates the app and launches it"
    app = Flask(__name__, instance_relative_config=False)

    logging.basicConfig(
        filename='variance.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    if test_config is None:
        app.config.from_object("variance.config.DevConfig")
    else:
        app.config.from_object(test_config)

    logging.info("Variance configuration loaded.")

    setup_instance_path(app.instance_path)

    rest_api = Api(app)

    load_models(app)

    load_cli(app)

    load_api(rest_api)

    db.init_app(app)

    logging.info("Variance AppDB init done.")
 
    @app.before_first_request
    def load_def_settings():
        load_default_settings(app)

    return app
