import functools
from flask import (
    current_app, g, request
)
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from variance.db import get_db
from variance.api.auth import login_required

class MuscleList(Resource):
    @login_required
    def post(self):
        db = get_db()
        pass

    def get(self):
        parser = RequestParser()
        args = parser.parse_args()
        db = get_db()
        pass

class Muscle(Resource):
    def get(self, muscle_id):
        db = get_db()
        pass

    @login_required
    def put(self, equipment_id):
        parser = RequestParser()
        args = parser.parse_args()
        db = get_db()
        pass
