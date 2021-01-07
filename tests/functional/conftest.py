import pytest
from variance import config, create_app, db

@pytest.fixture(scope="session")
def app():
    app = create_app(config.UnitTestConfig)
    print("App fixture")
    return app

@pytest.fixture(scope="session")
@pytest.mark.usefixtures("app")
def database(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


@pytest.fixture(scope="session")
@pytest.mark.usefixtures("database")
def user_token(app):
    with app.test_client() as client:
        # This is a test fixture that provides function tests with a JSON Web Token associated with a user that has only "user" roles
        r = client.post("/api/auth/register", 
            data={
                "username":"unit_test_user",
                "password":"passw0rd",
                "birthdate":"2002-07-18"
            })
        assert "id" in r.get_json()
        assert r.status_code == 201

        r = client.post("/api/auth/token",
            data={
                "username":"unit_test_user",
                "password":"passw0rd"
            })
        assert r.status_code == 200
        assert "token" in r.get_json()

        return r.get_json()["token"]