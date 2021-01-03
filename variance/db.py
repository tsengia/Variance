import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_URI"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory  = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("sql_scripts/schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))

def drop_all():
    db = get_db()
    with current_app.open_resource("sql_scripts/drop_all.sql") as f:
        db.executescript(f.read().decode("utf-8"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

@click.command("drop-all")
@with_appcontext
def drop_all_command():
    drop_all()
    click.echo("Dropped all tables from database.")

@click.command("add-default-units")
@with_appcontext
def default_units_command():
    db = get_db()
    with current_app.open_resource("sql_scripts/defaults/add_default_units.sql") as f:
        db.executescript(f.read().decode("utf-8"))
        click.echo("Default units added.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(default_units_command)


