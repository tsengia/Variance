import pathlib 
from flask import Flask
from flask_restful import Api, Resource

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    
    if test_config is None:
        app.config.from_object("config.DevConfig", silent=False)
    else:
        app.config.from_mapping(test_config)

    pathlib.Path(app.instance_path).mkdir(exist_ok=True)
    if not pathlib.Path(app.instance_path).is_dir():
        print("Instance directory could not be created! Exiting.")
        exit()

    from . import db
    db.init_app(app)

    api = Api(app)

    from .api import auth, units, equipment
    app.register_blueprint(auth.bp)
    api.add_resource(units.UnitList,    "/api/units/")
    api.add_resource(units.Unit,     "/api/units/<int:unit_id>")
    #api.add_resource(equipment.EquipmentList,      "/api/equipment/")
    #api.add_resource(equipment.Equipment,      "/api/equipment/<int:equipment_id>")


    @app.route("/api/apiversion")
    def api_verison():
        return { "apiversion": "0.1" }

    @app.route("/api/version")
    def version():
        return { "version":"0.0.1 alpha" }

    return app
