from pathlib import Path
import click
from flask.cli import AppGroup
from flask import current_app
from variance import db

db_cli = AppGroup("db")

@db_cli.command("drop-all")
def cli_db_drop_all():
    click.echo("Dropping all tables from database...")
    db.drop_all()
    click.echo("All tables dropped.")

@db_cli.command("init")
def cli_db_init():
    click.echo("Initializing database...")
    db.create_all()
    click.echo("Database initialized.")
