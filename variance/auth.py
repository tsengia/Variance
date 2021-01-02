import functools
import datetime

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from variance.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        birthday = request.form["birthday"]
        db = get_db()

        if not username:
            return {"error":"You must specify a username!"}
        elif not password:
            return {"error":"You must specify a password!"}
        elif not birthday:
            return {"error":"You must specify a birthday!"}
        try:
            birthday = datetime.date.fromisoformat(birthday)
        except ValueError:
            return {"error":"Birthday is not in a valid YYYY-MM-DD format!"}
            
        if db.execute("SELECT id FROM UserIndex WHERE username = ?", (username,)).fetchone() is not None:
            return {"error":"That username is already taken!"}
        db.execute("INSERT INTO UserIndex (username, password, birthdate) VALUES (?, ?, ?)", (username, generate_password_hash(password), birthday))
        db.commit()

        user = db.execute("SELECT * FROM UserIndex WHERE username = ?", (username,)).fetchone()

        return { "uid":str(user["id"]) }
