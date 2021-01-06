import pytest

@pytest.mark.usefixtures("database")
def test_registration_and_login(client): 
    r = client.post("/api/auth/register", 
            data={
                "username":"test2",
                "password":"passw0rd",
                "birthdate":"2002-07-18"
            })
    print("LOOK HERE DUDE:")
    print(r.data)
    """
    self.assertEqual("uid" in r.get_json(), True)

    r = test_client.post("/api/auth/login", 
            data={
                "username":"test2",
                "password":"passw0rd"
            })
    token = r.get_json()
    self.assertEqual(token is not None, True)
    """
