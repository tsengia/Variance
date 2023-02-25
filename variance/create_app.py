"""
Main entry point for Variance when running as a webserver
"""
import pathlib
import logging
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api, Blueprint

from variance.extensions import db

def setup_instance_path(instance_path):
    "Setup the instance directory structure"
    instance_path = pathlib.Path(instance_path)
    if not instance_path.exists():
        instance_path.mkdir(exist_ok=True)
        if not instance_path.is_dir():
            print("Instance directory could not be created! Exiting.")
            exit()
        logging.info("Created new instance directory")

def load_models(app):
    "Helper function that imports all the models"
    from variance.models import unit, muscle, equipment, exercise, gym, tracker, user, lambda_measure, workout, nutrition, mealplan
    logging.info("Variance Models imported.")

def load_cli(app):
    "Helper function that imports all the CLI commands"
    from variance import cli
    c = app.cli
    c.add_command(cli.db.db_cli)
    
    c.add_command(cli.all_cli)
    c.add_command(cli.setting.setting_cli)
    cli.user.user_cli.attach(c)
    cli.equipment.equipment_cli.attach(c)
    cli.muscle.muscle_cli.attach(c)
    cli.gym.gym_cli.attach(c)
    cli.exercise.exercise_cli.attach(c)
    cli.unit.unit_cli.attach(c)
    cli.tracker.tracker_cli.attach(c)
    cli.nutrient.nutrient_cli.attach(c)
    cli.consumable.consumable_cli.attach(c)

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

    api.units.units_endpoint.attach(rest_api, url_prefix="/api/")
    api.exercises.exercises_endpoint.attach(rest_api, url_prefix="/api/")
    api.muscles.muscle_endpoint.attach(rest_api, url_prefix="/api/")
    api.muscles.muscle_groups_endpoint.attach(rest_api, url_prefix="/api/")
    api.equipment.equipment_endpoint.attach(rest_api, url_prefix="/api/")
    api.trackers.trackers_endpoint.attach(rest_api, url_prefix="/api/")
    api.nutrients.nutrient_info_endpoint.attach(rest_api, url_prefix="/api/")
    api.consumables.consumable_endpoint.attach(rest_api, url_prefix="/api/")
    api.recipes.recipe_endpoint.attach(rest_api, url_prefix="/api/")
    api.settings.global_settings_endpoint.attach(rest_api, url_prefix="/api/")
    api.settings.user_settings_endpoint.attach(rest_api, url_prefix="/api/")

    logging.info("Variance API blueprints loaded.")

def create_app(test_config=None):
    "Main entry point, creates the app and launches it"
    app = Flask(__name__, instance_relative_config=False, static_url_path="/app")

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

    load_cli(app)

    load_models(app)

    load_api(rest_api)

    db.init_app(app)

    logging.info("Variance AppDB init done.")

    return app
