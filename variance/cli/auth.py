import click
from flask.cli import AppGroup
from variance.db import get_db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

auth_cli = AppGroup("auth")

@auth_cli.command("add")
@click.argument("username")
@click.argument("password")
@click.argument("birthday")
@click.option("-r","--role", "role", default=0, type=int)
def cli_create_user(username, password, birthday, role):
    db = get_db()
    if db.execute("SELECT id FROM UserIndex WHERE username=?", (username,)).fetchone() is not None:
        click.echo("A user with this username already exists!")
        return -1
    try:
        birthday = datetime.date.fromisoformat(birthday)
    except ValueError:
        click.echo("The birthday must be in YYYY-MM-DD format!")
    db.execute("INSERT INTO UserIndex (username, password, birthdate, role) VALUES (?, ?, ?, ?)", (username, generate_password_hash(password), birthday, role))
    db.commit()
    click.echo("User created.")

@auth_cli.command("del")
@click.argument("username")
def cli_delete_user(username):
    db = get_db()
    
    if db.execute("SELECT id FROM UserIndex WHERE username=?", (username,)).fetchone() is None:
        click.echo("No user found.")
        return -1

    db.execute("DELETE FROM UserIndex WHERE username=?", (username,))
    db.commit()
    
    click.echo("User deleted.")