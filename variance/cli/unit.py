import click
from flask.cli import AppGroup

from variance import db
from variance.models.unit import UnitModel

unit_cli = AppGroup("unit")
unit_mod_cli = AppGroup("mod")
unit_cli.add_command(unit_mod_cli)

@unit_cli.command("list")
def cli_unit_list():
    u_list = UnitModel.query.all()
    if u_list is None:
        click.echo("Unit list is empty!")
        return -1
    for u in u_list:
        click.echo(str(u))

@unit_cli.command("view")
@click.argument("id")
def cli_unit_view(id):
    u = UnitModel.query.get(id)
    if u is None:
        click.echo("Could not find an unit with that ID!")
        return -1
    click.echo(str(u))