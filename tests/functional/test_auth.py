import pathlib
from datetime import date
from unittest import TestCase

import variance
from variance import db

import config
import flask

app = None

def setUpModule():
    global app
    #print("Auth Setup called")
    app = variance.create_app(config.UnitTestConfig)

def tearDownModule():
	#print("Auth Tear down called")
    pass

class LifeCycleTest(TestCase):
    def test_registration_and_login(self):
        global app
        with app.test_client() as c: 
            r = c.post("/api/auth/register", 
                    data={
                        "username":"test2",
                        "password":"passw0rd",
                        "birthday":"2002-07-18"
                    })
            """
            self.assertEqual("uid" in r.get_json(), True)

            r = c.post("/api/auth/login", 
                    data={
                        "username":"test2",
                        "password":"passw0rd"
                    })
            token = r.get_json()
            self.assertEqual(token is not None, True)
            """