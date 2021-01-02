import functools
import datetime

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from variance.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    db = get_db()

    user = db.execute("SELECT * FROM UserIndex WHERE username=?", (username,)).fetchone()
    if user is None:
        return { "error":"Incorrect username or password!" }
    elif not check_password_hash(user["password"], password):
        return { "error":"Incorrect username or password!" }

    session.clear()
    session["user_id"] = user["id"]
    return { "uid":user["id"], "message":"Logged in." }

@bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    birthday = request.form.get("birthday", None)
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
