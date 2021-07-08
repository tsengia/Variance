import pytest

def test_new_unit(app_with_default_units, client, user_token):
    r = client.post("/api/units/",
                    data={
                        "token": user_token,
                        "name": "Test unit.",
                        "abbreviation": "tu",
                        "dimension": "test_dimension1"
                    })
    assert r.status_code == 201

    r = client.post("/api/units/",
                    data={
                        "token": user_token,
                        "name": "Test unit 2.",
                        "abbreviation": "tu2",
                        "dimension": "test_dimension1"
                    })
    assert r.status_code == 201

    r = client.get("/api/units/?count=4")
    print(r.data)
    assert r.status_code == 200
    assert len(r.get_json()) == 2
    print(r.get_json())
    assert r.get_json()[0]["name"] == "Test unit."
    assert r.get_json()[1]["name"] == "Test unit 2."

    r = client.post("/api/units/",
                    data={
                        "token": user_token,
                        "name": "Test unit 2.",
                        "abbreviation": "tu2",
                        "dimension": "test_dimension1"
                    })
    assert r.status_code == 409

    r = client.post("/api/units/",
                    data={
                        "token": user_token,
                        "name": "Test unit 3.",
                        "abbreviation": "tu3",
                        "dimension": "test_dimension2"
                    })

    r = client.get("/api/units/?dimension=test_dimension1&count=1")
    assert r.status_code == 200
    assert len(r.get_json()) == 1
    for u in r.get_json():
        assert u["dimension"] == "test_dimension1"

    r = client.get("/api/units/?dimension=test_dimension2")
    assert r.status_code == 200
    assert len(r.get_json()) == 1
    for u in r.get_json():
        assert u["dimension"] == "test_dimension2"

    r = client.get("/api/units/1")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Test unit."
    assert r.get_json()["abbreviation"] == "tu"
    assert r.get_json()["dimension"] == "test_dimension1"

    r = client.get("/api/units/3")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Test unit 3."
    assert r.get_json()["abbreviation"] == "tu3"
    assert r.get_json()["dimension"] == "test_dimension2"

    r = client.get("/api/units/4")
    assert r.status_code == 404

    # Attempt an upate without logging in
    r = client.post("/api/units/2", data={"name": "Renamed unit"})
    assert r.status_code == 401

    # Update while logged in
    r = client.post("/api/units/2",
                    data={
                        "token": user_token,
                        "name": "Renamed unit"
                    })
    assert r.status_code == 200

    # Assert that update succeeded
    r = client.get("/api/units/2")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Renamed unit"
    assert r.get_json()["abbreviation"] == "tu2"
    assert r.get_json()["multiplier"] == 1.0

    # Update while logged in, conflicting names
    r = client.post(
        "/api/units/1", data={"token": user_token, "name": "Renamed unit"})
    assert r.status_code == 409

    # Update while logged in, nonsense form
    r = client.post(
        "/api/units/1", data={"token": user_token, "dimension": "mass", "hello": "world"})
    assert r.status_code == 200

    # Attempt deletion without being logged in
    r = client.delete("/api/units/2")
    assert r.status_code == 401

    # Delete while logged in
    r = client.delete("/api/units/2", data={"token": user_token})
    assert r.status_code == 200

    # Make sure it was deleted
    r = client.get("/api/units/2")
    assert r.status_code == 404
