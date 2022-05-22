import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.nutrition import ConsumableModel

consumable_cli = AppGroup("consumable")
consumable_mod_cli = AppGroup("mod")
consumable_cli.add_command(consumable_mod_cli)


@consumable_cli.command("list")
def cli_consumable_list():
    c_list = ConsumableModel.query.all()
    if c_list is None:
        click.echo("Consumable list is empty!")
        return -1
    for c in c_list:
        click.echo(str(c))


@consumable_cli.command("view")
@click.argument("id")
def cli_consumable_view(id):
    c = ConsumableModel.query.get(id)
    if c is None:
        click.echo("Could not find an consumable with that ID!")
        return -1
    click.echo(str(c))
