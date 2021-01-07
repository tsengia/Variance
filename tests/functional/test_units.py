import pytest

def test_new_unit(client, user_token):
    r = client.post("/api/units/", 
        data={
            "token": user_token,
            "name":"Test unit.",
            "abbreviation":"tu",
            "dimension":"test_dimension1"
        })
    assert r.status_code == 201
    
    r = client.post("/api/units/", 
        data={
            "token": user_token,
            "name":"Test unit 2.",
            "abbreviation":"tu2",
            "dimension":"test_dimension1"
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
            "name":"Test unit 2.",
            "abbreviation":"tu2",
            "dimension":"test_dimension1"
        })
    assert r.status_code == 409
    
    r = client.post("/api/units/", 
        data={
            "token": user_token,
            "name":"Test unit 3.",
            "abbreviation":"tu3",
            "dimension":"test_dimension2"
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