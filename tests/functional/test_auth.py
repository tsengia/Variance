import pytest

@pytest.mark.usefixtures("database")
def test_good_registration(client): 
    r = client.post("/api/auth/register", 
            data={
                "username":"test2",
                "password":"asdfghjkl",
                "birthdate":"2012-03-10"
            })
    assert r.status_code == 201
    assert "id" in r.get_json()
    
@pytest.mark.usefixtures("database")
def test_bad_birthdate_registration(client): 
    r = client.post("/api/auth/register", 
            data={
                "username":"test2",
                "password":"asdfghjkl",
                "birthdate":"2012/234/2"
            })
    assert r.status_code == 422
    assert "status" in r.get_json()
