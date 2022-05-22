from pathlib import Path

import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.unit import UnitModel
from variance.schemas.unit import UnitSchema

from variance.models.muscle import MuscleModel
from variance.schemas.muscle import MuscleSchema


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
    export_dir.mkdir(exist_ok=True)
    unit_export_dir = export_dir / "units"
    unit_export_dir.mkdir()
    unit_dump_schema = UnitSchema(exclude=("id",))
    for u in u_list:
        cname = u.canonical_name
        unit_file = unit_export_dir / (cname + ".json")
        unit_file.write_text(str(unit_dump_schema.dump(u)))


@export_cli.command("muscles")
def cli_export_list():
    m_list = MuscleModel.query.all()
    if m_list is None:
        click.echo("Muscle list is empty!")
        return -1
    export_dir = Path("exported")
    export_dir.mkdir(exist_ok=True)
    muscle_export_dir = export_dir / "muscles"
    muscle_export_dir.mkdir()
    muscle_dump_schema = MuscleSchema(exclude=("id",))
    for m in m_list:
        cname = m.canonical_name
        muscle_file = muscle_export_dir / (cname + ".json")
        muscle_file.write_text(str(muscle_dump_schema.dump(m)))

