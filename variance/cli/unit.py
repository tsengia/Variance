from pathlib import Path
import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.unit import UnitModel
from variance.schemas.unit import UnitSchema

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

def count_units():
    return UnitModel.query.count()

@unit_cli.command("count")
def cli_unit_count():
    click.echo("There are {i} units in the database.".format(i=count_units()))

@unit_cli.command("export")
def cli_unit_export():
    u_list = UnitModel.query.all()
    if u_list is None:
        click.echo("Unit list is empty!")
        return -1
    export_dir = Path("exported")
    export_dir.mkdir(exist_ok=True)
    unit_export_dir = export_dir / "units"
    unit_export_dir.mkdir()
    unit_dump_schema = UnitSchema(exclude=("id",))
    for u in u_list:
        cname = u.canonical_name
        unit_file = unit_export_dir / (cname + ".json")
        unit_file.write_text(unit_dump_schema.dumps(u))


@unit_cli.command("import")
def cli_unit_import():
    click.echo("Importing units")
    import_dir = Path("imported")
    unit_import_dir = import_dir / "units"
    unit_load_schema = UnitSchema(exclude=("id",))
    i = 0
    for j in unit_import_dir.glob("*.json"):
        data, errors = unit_load_schema.loads(j.read_text())
        if errors:
            click.echo("ERROR")
        u = UnitModel(data)
        db.session.add(u)
        i += 1
    
    db.session.commit()
    click.echo("Imported {i} units.".format(i=count))
