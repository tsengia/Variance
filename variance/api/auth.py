import functools
import datetime
import jwt
import click
from flask import (
    current_app, Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from variance.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.cli.command("adduser")
@click.argument("username")
@click.argument("password")
@click.argument("birthday")
@click.option("-r","--role", "role", default=0, type=int)
def cli_create_user(username, password, birthday, role):
    db = get_db()
    if db.execute("SELECT id FROM UserIndex WHERE id=?", (username,)).fetchone() is not None:
        click.echo("A user with this username already exists!")
        return -1
    try:
        birthday = datetime.date.fromisoformat(birthday)
    except ValueError:
        click.echo("The birthday must be in YYYY-MM-DD format!")
    db.execute("INSERT INTO UserIndex (username, password, birthdate, role) VALUES (?, ?, ?, ?)", (username, generate_password_hash(password), birthday, role))
    db.commit()
    click.echo("User created.")

@bp.cli.command("deluser")
@click.argument("username")
def cli_delete_user(username):
    db = get_db()
    
    if db.execute("SELECT id FROM UserIndex WHERE username=?", (username,)).fetchone() is None:
        click.echo("No user found.")
        return -1

    db.execute("DELETE FROM UserIndex WHERE username=?", (username,))
    db.commit()
    
    click.echo("User deleted.")

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
    token = jwt.encode({"user_id":user["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config["SECRET_KEY"])
    return {"token":token}

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

@bp.route("/logout", methods=["POST", "GET"])
def logout():
    
    session.clear()
    return { "message":"Logged out." }

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
        token = request.values.get("token", None)
        if token is not None:
            try:
                decoded_token = jwt.decode(token, current_app.config["SECRET_KEY"])
                user_id = decoded_token["user_id"]
            except:
                current_app.logger.warn("User attempted to use an invalid token!")
    if user_id is not None:
        g.user = get_db().execute("SELECT * FROM UserIndex WHERE id=?", (user_id,))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return {"error":"You must be logged in to access this endpoint!"}
        return view(**kwargs)

    return wrapped_view
