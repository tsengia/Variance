import pathlib
from datetime import date
from unittest import TestCase

from context import variance
from variance import create_app, db

import debug_config

class LifeCycleTest(TestCase):
    def setUp(self):
        self.app = variance.create_app(debug_config.config)
        with self.app.app_context():
            db.init_db()

    def tearDown(self):
        pass

    def test_registration_and_login(self):
        with self.app.test_client() as c:
            r = c.post("/auth/register", data={"username":"test1", "password":"passw0rd", "birthday":"2002-07-18"})
            json_data = r.get_json()
            self.assertEqual(1, int(json_data["uid"]))
            
            r = c.post("/auth/register", data={"username":"test2", "password":"passw0rd2", "birthday":"2001-08-19"})
            json_data = r.get_json()
            self.assertEqual(2, int(json_data["uid"]))

            r = c.post("/auth/login", data={"username":"test1", "password":"passw0rd"})
            json_data = r.get_json()
            self.assertEqual(1, json_data["uid"])

        with self.app.test_client() as c2:
            r = c.post("/auth/register", data={"username":"test1", "password":"passw0rd", "birthday":"2002-07-18"})
            json_data = r.get_json()
            self.assertEqual("That username is already taken!", json_data["error"])
            
            r = c2.post("/auth/register", data={"u":"2", "password":"passw0rd", "birthday":"2002-07-18"})
            json_data = r.get_json()
            self.assertEqual("You must specify a username!", json_data["error"])

            r = c2.post("/auth/register", data={"username":"test1", "birthday":"2002-07-18"})
            json_data = r.get_json()
            self.assertEqual("You must specify a password!", json_data["error"])
            
            r = c2.post("/auth/register", data={"username":"test1", "password":"passw0rd"})
            json_data = r.get_json()
            self.assertEqual("You must specify a birthday!", json_data["error"])
