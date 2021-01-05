import click
from flask.cli import AppGroup
from variance.db import get_db

muscles_cli = AppGroup("muscles")

@muscles_cli.command("add")
@click.argument("name")
@click.option("-d", "--description", "description", default="", type=str)
def cli_add_muscle(name, description):
    db = get_db()
    if db.execute("SELECT id FROM MuscleIndex WHERE name=?", (name,)).fetchone() is not None:
        click.echo("An muscle with that name already exists!")
        return -1
    db.execute("INSERT INTO MuscleIndex (name, description) VALUES (?, ?)", (name, description))
    db.commit()
    click.echo("Muscle created!")

@muscles_cli.command("del")
@click.argument("name")
def cli_delete_muscle(name):
    db = get_db()
    
    if db.execute("SELECT id FROM MuscleIndex WHERE name=?", (name,)).fetchone() is None:
        click.echo("No muscle with that name found!")
        return -1

    db.execute("DELETE FROM MuscleIndex WHERE name=?", (name,))
    db.commit()
    
    click.echo("Equipment deleted.")