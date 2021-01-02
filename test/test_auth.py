import pathlib
from datetime import date
from unittest import TestCase

from context import variance
from variance import create_app, db

import debug_config

class RegistrationTest(TestCase):
    def setUp(self):
        self.app = variance.create_app(debug_config.config)

    def tearDown(self):
        pass

    def test_registration(self):
        with self.app.test_client() as c:
            r = c.post("/auth/register", data={"username":"test1", "password":"passw0rd", "birthday":"2002-07-18"})
            self.assertEqual(r.data, '{"uid":"0"}')
