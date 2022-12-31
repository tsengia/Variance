import pytest

"""
def test_good_registration(app_with_defaults, client):
    r = client.post("/api/auth/register",
                    data={
                        "username": "test3",
                        "password": "asdfghjkl",
                        "birthdate": "2012-03-10"
                    })
    assert r.status_code == 201
    assert "id" in r.get_json()

def test_bad_birthdate_registration(app_with_defaults, client):
    r = client.post("/api/auth/register",
                    data={
                        "username": "test3",
                        "password": "asdfghjkl",
                        "birthdate": "2012/234/2"
                    })
    assert r.status_code == 422
    assert "status" in r.get_json()

def test_short_password_registration(app_with_defaults, client):
    r = client.post("/api/auth/register",
                    data={
                        "username": "shortpassword",
                        "password": "123",
                        "birthdate": "2014-03-10"
                    })
    assert r.status_code == 422
    assert "message" in r.get_json()

def test_bad_username_registration(app_with_defaults, client):
    r = client.post("/api/auth/register",
                    data={
                        "username": "oh",
                        "password": "123456789",
                        "birthdate": "2014-03-10"
                    })
    assert r.status_code == 422
    assert "message" in r.get_json()

    r = client.post("/api/auth/register",
                    data={
                        "username": "abcdefgh123[]oops",
                        "password": "123456789",
                        "birthdate": "2014-03-10"
                    })
    assert r.status_code == 422
    assert "message" in r.get_json()

    r = client.post("/api/auth/register",
                    data={
                        "username": "ThisIsALongUsernameThatIsMoreThan21Chars",
                        "password": "123456789",
                        "birthdate": "2014-03-10"
                    })
    assert r.status_code == 422
    assert "message" in r.get_json()


def test_duplicate_registration(app_with_defaults, client):
    # First username, should succeed
    r = client.post("/api/auth/register",
                    data={
                        "username": "test4",
                        "password": "asdfghjkl",
                        "birthdate": "2014-03-10"
                    })
    assert r.status_code == 201
    assert "id" in r.get_json()

    # Duplicate username, should error out
    r = client.post("/api/auth/register",
                    data={
                        "username": "test4",
                        "password": "asdfghjkl",
                        "birthdate": "2014-03-10"
                    })
    assert r.status_code == 409
    assert "message" in r.get_json()

    # Another duplicate username, should error out
    r = client.post("/api/auth/register",
                    data={
                        "username": "test4",
                        "password": "ery3456i",
                        "birthdate": "2011-02-10"
                    })
    assert r.status_code == 409
    assert "message" in r.get_json()
"""