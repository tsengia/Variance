import pytest
from variance import config, create_app, db

@pytest.fixture
def app():
    app = create_app(config.UnitTestConfig)
    print("App fixture")
    return app

@pytest.fixture
@pytest.mark.usefixtures("app")
def database(app):
    print("database fixture")
    db.create_all()