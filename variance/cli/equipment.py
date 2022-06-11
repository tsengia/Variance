from pathlib import Path
import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.equipment import EquipmentModel
from variance.schemas.equipment import EquipmentSchema

equipment_cli = AppGroup("equipment")
equipment_mod_cli = AppGroup("mod")
equipment_cli.add_command(equipment_mod_cli)

@equipment_cli.command("get")
@click.argument("name")
def cli_equipment_get(name):
    u = EquipmentModel.query.filter_by(name=name).first()
    if u is None:
        click.echo("No equipment with that name found!")
        return -1
    click.echo("Equipment ID: %u" % u.id)


@equipment_cli.command("list")
def cli_equipment_list():
    e_list = EquipmentModel.query.all()
    if e_list is None:
        click.echo("Equipment list is empty!")
        return -1
    for a in e_list:
        click.echo("%u : %s - %s" % (a.id, a.name, a.description))


@equipment_cli.command("add")
@click.argument("name")
@click.argument("description")
def cli_user_add(name, description):
    u = EquipmentModel.query.filter_by(name=name).first()
    if u is not None:
        click.echo("An equipment with that name already exists!")
        return -1
    new_equipment = EquipmentModel(name=name, description=description)
    db.session.add(new_equipment)
    db.session.commit()
    click.echo("Equipment (%s) added." % (name))


@equipment_cli.command("del")
@click.argument("equipment_id")
def cli_user_del(equipment_id):
    u = EquipmentModel.query.get(equipment_id)
    if u is None:
        click.echo("No equipment with that ID found!")
        return -1
    name = u.name
    db.session.delete(u)
    db.session.commit()
    click.echo("Equipment %u (%s) deleted." % (equipment_id, name))


@equipment_cli.command("export")
def cli_equipment_export():
    e_list = EquipmentModel.query.all()
    if e_list is None:
        click.echo("Equipment list is empty!")
        return -1
    export_dir = Path("exported")
    export_dir.mkdir(exist_ok=True)
    equipment_export_dir = export_dir / "equipment"
    equipment_export_dir.mkdir()
    equipment_dump_schema = EquipmentSchema(exclude=("id",))
    for e in e_list:
        cname = e.canonical_name
        equipment_file = equipment_export_dir / (cname + ".json")
        equipment_file.write_text(equipment_dump_schema.dumps(e))
