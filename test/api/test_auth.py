import pathlib
from datetime import date
from unittest import TestCase

from context import variance
from variance import create_app, db

import config
import flask

class LifeCycleTest(TestCase):
    def setUp(self):
        self.app = variance.create_app(config.UnitTestConfig)
        with self.app.app_context():
            db.init_db()

    def tearDown(self):
        pass

    def test_registration_and_login(self):
        with self.app.test_client() as c: 
            r = c.post("/api/auth/register", data={"username":"test2", "password":"passw0rd", "birthday":"2002-07-18"})
            self.assertEqual("uid" in r.get_json(), True)

            r = c.post("/api/auth/login", data={"username":"test2", "password":"passw0rd"})
            token = r.get_json()
            self.assertEqual(token is not None, True)


