import pytest
from variance import config, create_app
from variance.extensions import db

@pytest.fixture(scope="session")
def app():
    app = create_app.create_app(config.UnitTestConfig)
    return app

@pytest.fixture(scope="session")
def app_with_database(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

@pytest.fixture(scope="session")
def app_with_defaults(app_with_database):
    with app_with_database.app_context() as ctx:
        from variance.cli import resource_command_list
        for c in resource_command_list:
            c.import_data("variance/fixtures")
    return app_with_database
