import pytest
from variance import config, create_app, db
from variance.cli.load_fixtures import fixture_load_units

@pytest.fixture(scope="session")
def app():
    app = create_app(config.UnitTestConfig)
    print("App fixture")
    return app


@pytest.fixture(scope="session")
def app_with_database(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
    

@pytest.fixture(scope="session")
def app_with_default_units(app_with_database):
    with app_with_database.app_context():
        fixture_load_units()
    return app_with_database

@pytest.fixture(scope="session")
def user_token(app_with_default_units):
    with app_with_default_units.test_client() as client:
        # This is a test fixture that provides function tests with a JSON Web Token associated with a user that has only "user" roles
        r = client.post("/api/auth/register",
                        data={
                            "username": "unit_test_user",
                            "password": "passw0rd",
                            "birthdate": "2002-07-18"
                        })
        assert "id" in r.get_json()
        assert r.status_code == 201

        r = client.post("/api/auth/token",
                        data={
                            "username": "unit_test_user",
                            "password": "passw0rd"
                        })
        assert r.status_code == 200
        assert "token" in r.get_json()

        return r.get_json()["token"]
