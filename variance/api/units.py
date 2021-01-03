import functools
from flask import (
        current_app, g, request
)
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from variance.db import get_db
from variance.api.auth import login_required

class UnitList(Resource):
    @login_required
    def post(self): # Create a new unit
        args = self.get_parser.parse_args()
        db = get_db()

        if db.execute("SELECT id FROM UnitIndex WHERE name=?", (args["name"],)).fetchone() is not None:
            return {"error":"A unit with that name already exists!" }, 409

        db.execute("INSERT INTO UnitIndex (name, abbreviation, dimension) VALUES (?, ?, ?)", (args["name"], args["abbreviation"], args["dimension"]))
        db.commit()
        return {"status":"Unit created."}, 201


    def get(self): # List all units
        args = self.get_parser.parse_args()
        db = get_db()
        units = []
        if args["count"] is not None:
            if args["dimension"] is not None:
                rows = db.execute("SELECT * FROM UnitIndex WHERE dimension=? LIMIT ? OFFSET ?", (args["dimension"], args["count"], args["offset"])).fetchall()
            else:
                rows = db.execute("SELECT * FROM UnitIndex LIMIT ? OFFSET ?", (args["count"], args["offset"])).fetchall()
        elif args["dimension"] is not None:
            rows = db.execute("SELECT * FROM UnitIndex WHERE dimension=?", (args["dimension"],)).fetchall()
        else:
            rows = db.execute("SELECT * FROM UnitIndex").fetchall()

        for u in rows:
            units.append({"id":u["id"], "name":u["name"],"abbreviation":u["abbreviation"],"dimension":u["dimension"]})

        return { "units":units }, 200


    def __init__(self):
        self.get_parser = RequestParser()
        self.get_parser.add_argument("count", type=int)
        self.get_parser.add_argument("offset", type=int, default=0)
        self.get_parser.add_argument("dimension", type=str)

        self.post_parser = RequestParser()
        self.post_parser.add_argument("name", type=str, required=True)
        self.post_parser.add_argument("abbreviation", type=str, required=True)
        self.post_parser.add_argument("dimension", type=str, required=True)


class Unit(Resource):

    @login_required
    def post(self, unit_id): # Update a unit
        args = self.post_parser.parse_args()
        db = get_db()
        unit = db.execute("SELECT * FROM UnitIndex WHERE id=?", (unit_id,)).fetchone()
        if unit is None:
            return {"error":"No unit found with that ID!"}, 404

        if args["name"] is not None:
            if db.execute("SELECT id FROM UnitIndex WHERE name=?", (args["name"])).getone() is not None:
                return {"error":"A unit with that name already exists!"}, 409
        else:
            new_name = unit["name"]

        if args["dimension"] is not None:
            new_dimension = args["dimension"]
        else:
            new_dimension = unit["dimension"]

        if args["abbreviation"] is not None:
            new_abbreviation = args["abbreviation"]
        else:
            new_abbreviation = unit["abbreviation"]

        db.execute("UPDATE UnitIndex SET name=?,abbreviation=?,dimension=? WHERE id=?", (new_name, new_abbreviation, new_dimension, unit["id"]))
        db.commit()
        return {"status":"Unit updated."}

    def get(self, unit_id): # Display a unit
        unit = db.execute("SELECT * FROM UnitIndex WHERE id=?", (unit_id,)).fetchone()
        if unit is None:
            return {"error":"No unit found with that ID!"}, 404
        return { "id":unit["id"], "name":unit["name"], "abbreviation":unit["abbreviation"], "dimension":unit["dimension"] }

    def __init__(self):
        self.post_parser = RequestParser()
        self.get_parser.add_argument("name", type=str)
        self.get_parser.add_argument("dimension", type=str)
        self.get_parser.add_argument("abbreviation", type=str)

