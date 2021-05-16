import pathlib
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    
    logging.basicConfig(filename='variance.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    if test_config is None:
        app.config.from_object("variance.config.DevConfig")
    else:
        app.config.from_object(test_config)
        
    logging.info("Variance configuration loaded.")

    # Setup the instance directory structure
    pathlib.Path(app.instance_path).mkdir(exist_ok=True)
    if not pathlib.Path(app.instance_path).is_dir():
        print("Instance directory could not be created! Exiting.")
        exit()

    rest_api = Api(app)

    from variance.models import  unit, user, permissions, tracker, equipment, gym, nutrition, mealplan, workout, muscle, lambda_measure, exercise
    logging.info("Variance Models imported.")
    from variance import cli
    app.cli.add_command(cli.db.db_cli)
    app.cli.add_command(cli.permissions.permissions_cli)
    app.cli.add_command(cli.user.user_cli)
    app.cli.add_command(cli.equipment.equipment_cli)
    app.cli.add_command(cli.gym.gym_cli)
    app.cli.add_command(cli.muscle.muscle_cli)
    app.cli.add_command(cli.exercise.exercise_cli)
    app.cli.add_command(cli.unit.unit_cli)
    app.cli.add_command(cli.load_fixtures.lf_cli)
    """
    app.cli.add_command(cli.fixtures.fixtures_cli)
    app.cli.add_command(cli.units.units_cli)
    
    app.cli.add_command(cli.equipment.equipment_cli)
    app.cli.add_command(cli.muscles.muscles_cli)
    """
    
    logging.info("Variance CLI loaded.")

    from variance import api
    app.register_blueprint(api.auth.bp, url_prefix="/api/auth")
    app.register_blueprint(api.units.bp, url_prefix="/api/units")

    logging.info("Variance blueprints loaded.")

    db.init_app(app)
    
    logging.info("Variance AppDB init done.")

    @app.route("/api/apiversion")
    def api_verison():
        return { "apiversion": "0.1" }

    @app.route("/api/version")
    def version():
        return { "version":"0.0.1 alpha" }

    return app


