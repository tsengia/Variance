from pathlib import Path
import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.muscle import MuscleModel, MuscleGroupModel
from variance.schemas.muscle import MuscleSchema

muscle_cli = AppGroup("muscle")
muscle_group_cli = AppGroup("group")
muscle_mod_cli = AppGroup("mod")
muscle_cli.add_command(muscle_mod_cli)
muscle_cli.add_command(muscle_group_cli)


@muscle_cli.command("list")
def cli_muscle_list():
    m_list = MuscleModel.query.all()
    if m_list is None:
        click.echo("Muscle list is empty!")
        return -1
    for m in m_list:
        click.echo(str(m))


@muscle_group_cli.command("list")
def cli_muscle_group_list():
    mg_list = MuscleGroupModel.query.all()
    if mg_list is None:
        click.echo("MuscleGroup list is empty!")
        return -1
    for g in mg_list:
        click.echo(str(g))


@muscle_group_cli.command("view")
@click.argument("id")
def cli_muscle_group_view(id):
    mg = MuscleGroupModel.query.get(id)
    if not mg:
        click.echo("Could not find a MuscleGroup with that id!")
        return -1
    click.echo(str(mg))
    for m in mg.muscles:
        click.echo("\t->%u %s" % (m.id, m.name))

@muscle_cli.command("export")
def cli_muscle_export():
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
        muscle_file.write_text(muscle_dump_schema.dumps(m))
