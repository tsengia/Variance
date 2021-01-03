from pathlib import Path
import click
from flask.cli import AppGroup
from variance.db import get_db
from flask import current_app

db_cli = AppGroup("db")

@db_cli.command("init")
def cli_db_init():
    click.echo("Initializing database...")
    db = get_db()
    with current_app.open_resource("schema.sql") as s:
        db.executescript(s.read().decode("utf-8"))
    db.commit()
    click.echo("Database initialized.")