import pathlib
from datetime import date
from unittest import TestCase

from context import variance
from variance import create_app, db

import debug_config

class RegistrationTest(TestCase):
    def setUp(self):
        self.app = variance.create_app(debug_config.config)
        with self.app.app_context():
            db.init_db()

    def tearDown(self):
        pass

    def test_registration(self):
        with self.app.test_client() as c:
            r = c.post("/auth/register", data={"username":"test1", "password":"passw0rd", "birthday":"2002-07-18"})
            json_data = r.get_json()
            self.assertEqual(1, int(json_data["uid"]))
