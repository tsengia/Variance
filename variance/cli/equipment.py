import click
from flask.cli import AppGroup
from variance.db import get_db

equipment_cli = AppGroup("equipment")

@equipment_cli.command("add")
@click.argument("name")
@click.option("-d", "--description", "description", default="", type=str)
def cli_add_equipment(name, description):
    db = get_db()
    if db.execute("SELECT id FROM EquipmentIndex WHERE name=?", (name,)).fetchone() is not None:
        click.echo("An equipment with that name already exists!")
        return -1
    db.execute("INSERT INTO EquipmentIndex (name, description) VALUES (?, ?)", (name, description))
    db.commit()
    click.echo("Equipment created!")