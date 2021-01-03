import click
from flask.cli import AppGroup
from variance.db import get_db

units_cli = AppGroup("units")

@units_cli.command("add")
@click.argument("name")
@click.argument("abbreviation")
@click.argument("dimension")
def cli_add_unit(name, abbreviation, dimension):
    db = get_db()

    if db.execute("SELECT id FROM UnitIndex WHERE name=?", (name,)).fetchone() is not None:
        click.echo("A unit with that name already exists!")
        return -1

    db.execute("INSERT INTO UnitIndex (name, abbreviation, dimension) VALUES (?, ?, ?)", (name, abbreviation, dimension))
    db.commit()
    click.echo("Unit added.")

@units_cli.command("del")
@click.argument("name")
def cli_del_unit(name):
    db = get_db()

    unit = db.execute("SELECT id FROM UnitIndex WHERE name=?", (name,)).fetchone()
    if unit is None:
        click.echo("No unit with that name was found!")
        return -1
    db.execute("DELETE FROM UnitIndex WHERE name=?", (name,))
    db.commit()
    click.echo("Unit deleted.")