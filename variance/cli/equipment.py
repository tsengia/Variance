from variance.extensions import db

from variance.models.equipment import EquipmentModel
from variance.schemas.equipment import EquipmentSchema
from variance.cli.resource import ResourceCLI
from variance.common.util import canonize

import click

equipment_cli = ResourceCLI(EquipmentModel, EquipmentSchema, "Equipment", "equipment")

@equipment_cli.group.command("add")
@click.argument("name")
@click.argument("description")
def cli_equipment_add(name, description):
    e = EquipmentModel.query.filter_by(name=name).first()
    if e is not None:
        click.echo("An equipment with that name already exists!")
        return -1
    new_equipment = EquipmentModel(name=name, canonical_name=canonize(name), description=description)
    db.session.add(new_equipment)
    db.session.commit()
    click.echo("Equipment (%s) added." % (name))
    click.echo("UUID: %s" % (new_equipment.uuid))
