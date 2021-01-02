import functools
from flask import (
        current_app, Blueprint, g, session, request, jsonify
)

from variance.db import get_db
from variance.api.auth import login_required
from variance.units import *

bp = Blueprint("units", __name__, url_prefix="/api/units")

@bp.route("/", methods=["POST"])
@login_required
def new_unit():
    name = request.values.get("n", None)
    if not name:
        return {"error":"Parameter name (n) is missing!"}, 400
    abbreviation = request.values.get("a", None)
    if not abbreviation:
        return {"error":"Parameter abbreviation (a) is missing!" }, 400
    dimension = request.values.get("d", None)
    if not dimension:
        return {"error":"Parameter dimension (d) is missing!" }, 400
    
    db = get_db()
    if db.execute("SELECT id FROM UnitIndex WHERE name=?", (name,)).fetchone() is not None:
        return {"error":"A unit with that name already exists!" }, 409

    db.execute("INSERT INTO UnitIndex (name, abbreviation, dimension) VALUES (?, ?, ?)", (name, abbreviation, dimension))
    db.commit()
    return {"status":"Unit created."}, 201

@bp.route("/<int:unit_id>", methods=["GET", "POST"])
def show_unit(unit_id):
    db = get_db()
    unit = db.execute("SELECT * FROM UnitIndex WHERE id=?", (unit_id,)).fetchone()
    if unit is None:
        return {"error":"No unit found with that ID!"}, 404

    if request.method == "GET":
        return { "id":unit["id"], "name":unit["name"], "abbreviation":unit["abbreviation"], "dimension":unit["dimension"] }
    elif request.method == "POST":
        if g.user is None:
            return {"error":"You must be logged in to modify this endpoint!"}, 401

        new_abbreviation = request.form.get("a", unit["abbreviation"])
        new_dimension = request.form.get("d", unit["dimension"])
        new_name = request.form.get("n", None)

        if new_name:
            if db.execute("SELECT id FROM UnitIndex WHERE name=?", (new_name,)).getone() is not None:
                return {"error":"A unit with that name already exists!"}, 409
        else:
            new_name = unit["name"]

        db.execute("UPDATE UnitIndex SET name=?,abbreviation=?,dimension=? WHERE id=?", (new_name, new_abbreviation, new_dimension, unit["id"]))
        db.commit()
        return {"status":"Unit updated."}

@bp.route("/", methods=["GET"])
def list_units():
    count = request.values.get("c", None)
    dimension = request.values.get("d", None)
    offset = request.values.get("o", 0)
    db = get_db()

    units = []
    if count:
        try:
            count = int(count)
        except ValueError:
            return {"error":"Parameter count is invalid!"}

        if dimension: # dimension + count
            rows = db.execute("SELECT * FROM UnitIndex WHERE dimension=? LIMIT ? OFFSET ?", (dimension, count, offset)).fetchall()
        else: # count only
            rows = db.execute("SELECT * FROM UnitIndex LIMIT ? OFFSET ?", (count,offset)).fetchall()
    elif dimension is not None: # dimension only
        rows = db.execute("SELECT * FROM UnitIndex WHERE dimension=?", (dimension,)).fetchall()
    else: # no filters
        rows = db.execute("SELECT * FROM UnitIndex").fetchall()
    
    if len(rows) == 0:
        return "{}"

    for u in rows:
        units.append({"id":u["id"], "name":u["name"],"abbreviation":u["abbreviation"],"dimension":u["dimension"]})
    return {"units":units}
