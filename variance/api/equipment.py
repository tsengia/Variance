import functools
from flask import (
    current_app, g, request
)
import click
from flask.cli import AppGroup
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from variance.db import get_db
from variance.api.auth import login_required

class EquipmentList(Resource):
    @login_required
    def post(self):
        pass

    def get(self):
        parser = RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("count", type=int)
        parser.add_argument("offset", type=int, default=0)
        args = parser.parse_args()
        db = get_db()

        if args["name"] is not None:
            if args["count"] is not None:
                rows = db.execute("SELECT * FROM EquipmentIndex WHERE name LIKE ? LIMIT ? OFFSET ?", ("%" + args["name"] + "%", args["count"], args["offset"])).fetchall()
            else:
                rows = db.execute("SELECT * FROM EquipmentIndex WHERE name LIKE ?", ("%" + args["name"] + "%",)).fetchall()
        elif args["count"] is not None:
            rows = db.execute("SELECT * FROM EquipmentIndex LIMIT ? OFFSET ?", (args["count"], args["offset"])).fetchall()
        else:
            rows = db.execute("SELECT * FROM EquipmentIndex").fetchall()
            current_app.logger.info(str(len(rows)))

        equipment_list = []
        for r in rows:
            equipment_list.append({"id":r["id"],"name":r["name"],"description":r["description"]})

        return { "equipment":equipment_list }, 200

class Equipment(Resource):
    def get(self, equipment_id):
        db = get_db()
        equipment = db.execute("SELECT * FROM EquipmentIndex WHERE id=?", (equipment_id,)).fetchone()
        if equipment is None:
            return {"error":"No equipment with that ID found!"}, 404
        return { "id":equipment_id, "name":equipment["name"], "description":equipment["description"] }, 200

    @login_required
    def put(self, equipment_id):
        parser = RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("descriptio", type=str)
        args = parser.parse_args()
        db = get_db()

        equipment = db.execute("SELECT * FROM EquipmentIndex WHERE id=?", (equipment_id,)).fetchone()
        if equipment is None:
            return {"error":"No equipment found with what ID!"}, 404

        if args["name"] is not None:
            if db.execute("SELECT id FROM EquipmentIndex WHERE name=?", (args["name"],)).fetchone() is not None:
                return {"error":"An equipment with that name already exists!"}, 409
            new_name = args["name"]
        else:
            new_name = equipment["name"]

        if args["description"] is not None:
            new_description = args["description"]
        else:
            new_description = equipment["description"]

        db.execute("UPDATE EquipmentIndex (name, description) VALUES (?, ?) WHERE id=?", (new_name, new_description, equipment_id))
        db.commit()
        return {"status":"Equipment updated."}, 200
