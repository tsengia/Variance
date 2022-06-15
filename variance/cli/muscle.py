from pathlib import Path
import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.muscle import MuscleModel, MuscleGroupModel
from variance.schemas.muscle import MuscleSchema

from variance.common.json_export import export_models
from variance.common.json_import import import_models

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
    export_dir = Path("exported")
    export_dir.mkdir(exist_ok=True)
    muscle_export_dir = export_dir / "muscles"
    muscle_export_dir.mkdir(exist_ok=True)
    count = export_models(MuscleModel, MuscleSchema, muscle_export_dir)
    click.echo("Exported {i} MuscleModels.".format(i=count))

@muscle_cli.command("import")
def cli_muscle_import():
    click.echo("Importing muscles...")
    import_dir = Path("imported")
    muscle_import_dir = import_dir / "muscles"
    count = import_models(MuscleModel, MuscleSchema, muscle_import_dir, db.session)
    click.echo("Imported {i} MuscleModels.".format(i=count))
