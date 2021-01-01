import pathlib 
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=pathlib.Path(app.instance_path) / "variance.sqlite"
    )
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=False)
    else:
        app.config.from_mapping(test_config)

    
    pathlib.Path(app.instance_path).mkdir(exist_ok=True)
    if not pathlib.Path(app.instance_path).is_dir():
        print("Instance directory could not be created! Exiting.")
        exit()

    @app.route("/apiversion")
    def api_verison():
        return { "api_version": "0.1" }

    @app.route("/version")
    def version():
        return { "version":"0.0.1 alpha" }

    return app
