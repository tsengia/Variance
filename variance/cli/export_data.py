from pathlib import Path

import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.unit import UnitModel

export_cli = AppGroup("export")

@export_cli.command("all")
def cli_export_list():
    click.echo("Not implemented yet.")
    return

@export_cli.command("units")
def cli_export_list():
    u_list = UnitModel.query.all()
    if u_list is None:
        click.echo("Unit list is empty!")
        return -1
    export_dir = Path("exported")
    unit_export_dir = export_dir / "units"
    unit_export_dir.mkdir(parents=True)
    for u in u_list:
        cname = u.canonical_name
        click.echo(str(cname))

#@export_cli.command("view")
#@click.argument("id")
#def cli_export_view(id):
#    u = UnitModel.query.get(id)
#    if u is None:
#        click.echo("Could not find an export with that ID!")
#        return -1
#    click.echo(str(u))
