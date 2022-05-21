import pytest

def test_new_unit(app_with_defaults, user_token, admin_token):
    with app_with_defaults.test_client() as client:
        r = client.get("/api/units/")
        assert r.status_code == 200
        starting_number_of_units = len(r.get_json())
        
        r = client.post("/api/units/",
                        data={
                            "token": admin_token,
                            "name": "Test unit.",
                            "abbreviation": "tu",
                            "dimension": "test_dimension1"
                        })
        assert r.status_code == 201
        test_unit_1_id = str(r.get_json()["id"])

        r = client.post("/api/units/",
                        data={
                            "token": admin_token,
                            "name": "Test unit 2.",
                            "abbreviation": "tu2",
                            "dimension": "test_dimension1"
                        })
        assert r.status_code == 201
        test_unit_2_id = str(r.get_json()["id"])

        r = client.get("/api/units/?count=4&dimension=test_dimension1")
        print(r.data)
        assert r.status_code == 200
        assert len(r.get_json()) == 2
        print(r.get_json())
        assert r.get_json()[0]["name"] == "Test unit."
        assert r.get_json()[1]["name"] == "Test unit 2."

        r = client.post("/api/units/",
                        data={
                            "token": admin_token,
                            "name": "Test unit 2.",
                            "abbreviation": "tu2",
                            "dimension": "test_dimension1"
                        })
        assert r.status_code == 409

        r = client.post("/api/units/",
                        data={
                            "token": admin_token,
                            "name": "Test unit 3.",
                            "abbreviation": "tu3",
                            "dimension": "test_dimension2"
                        })
        test_unit_3_id = str(r.get_json()["id"])

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

        r = client.get("/api/units/" + test_unit_1_id)
        assert r.status_code == 200
        assert r.get_json()["name"] == "Test unit."
        assert r.get_json()["abbreviation"] == "tu"
        assert r.get_json()["dimension"] == "test_dimension1"

        r = client.get("/api/units/" + test_unit_3_id)
        assert r.status_code == 200
        assert r.get_json()["name"] == "Test unit 3."
        assert r.get_json()["abbreviation"] == "tu3"
        assert r.get_json()["dimension"] == "test_dimension2"

        r = client.get("/api/units/400")
        assert r.status_code == 404

        # Attempt an update without logging in
        r = client.post("/api/units/" + test_unit_2_id, data={"name": "Renamed unit"})
        assert r.status_code == 401

        # Update while logged in
        r = client.post("/api/units/" + test_unit_2_id,
                        data={
                            "token": admin_token,
                            "name": "Renamed unit"
                        })
        assert r.status_code == 200

        # Assert that update succeeded
        r = client.get("/api/units/" + test_unit_2_id)
        assert r.status_code == 200
        assert r.get_json()["name"] == "Renamed unit"
        assert r.get_json()["abbreviation"] == "tu2"
        assert r.get_json()["multiplier"] == 1.0

        # Update while logged in, conflicting names
        r = client.post(
            "/api/units/" + test_unit_1_id, data={"token": admin_token, "name": "Renamed unit"})
        assert r.status_code == 409

        # Update while logged in, nonsense form
        r = client.post(
            "/api/units/" + test_unit_1_id, data={"token": admin_token, "dimension": "mass", "hello": "world"})
        assert r.status_code == 200

        # Attempt deletion without being logged in
        r = client.delete("/api/units/" + test_unit_2_id)
        assert r.status_code == 401

        # Delete while logged in
        r = client.delete("/api/units/" + test_unit_2_id, data={"token": admin_token})
        assert r.status_code == 200

        # Make sure it was deleted
        r = client.get("/api/units/" + test_unit_2_id)
        assert r.status_code == 404
