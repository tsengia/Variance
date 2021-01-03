import functools
from flask import (
    current_app, Blueprint, g, session, request
)

from variance.db import get_db
from variance.api.auth import login_required

bp = Blueprint("equipment", __name__, url_prefix="/api/equipment")

@bp.route("/", methods=["POST"])
@login_required
def new_equipment():
    name = request.form.get("n", None)
    description = request.form.get("d", "")

    if not name:
        return {"error":"Missing name (n) parameter!"}, 400
    db = get_db()

    if db.execute("SELECT id FROM EquipmentIndex WHERE name=?", (name,)).fetchone() is not None:
        return {"error":"An equipment with that name already exists!"}, 409

    db.execute("INSERT INTO EquipmentIndex (name, description) VALUES (?, ?)", (name, description))
    db.commit()
    return {"status":"Equipment added."}, 201

@bp.route("/", methods=["GET"])
def list_equipment():
    count = request.form.get("c", None)
    offset = request.form.get("o", 0)
    db = get_db()
    
    if count:
        equipment = db.execute("SELECT * FROM EquipmentIndex LIMIT ? OFFSET ?", (count, offset)).fetchall()
    else:
        equipment = db.execute("SELECT * FROM EquipmentIndex").fetchall()

    a = []
    for e in equipment:
        a.append({"id":e["id"],"name":e["name"],"description":e["description"]})
    return { "equipment":a }
