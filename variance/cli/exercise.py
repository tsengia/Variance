from pathlib import Path
import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.exercise import ExerciseModel
from variance.schemas.exercise import ExerciseSchema

from variance.common.json_export import export_models
from variance.common.json_import import import_models

exercise_cli = AppGroup("exercise")
exercise_mod_cli = AppGroup("mod")
exercise_cli.add_command(exercise_mod_cli)


@exercise_cli.command("list")
def cli_exercise_list():
    e_list = ExerciseModel.query.all()
    if e_list is None:
        click.echo("Exercise list is empty!")
        return -1
    for e in e_list:
        click.echo(str(e))


@exercise_cli.command("view")
@click.argument("id")
def cli_exercise_view(id):
    e = ExerciseModel.query.get(id)
    if e is None:
        click.echo("Could not find an Exercise with that ID!")
        return -1
    click.echo(str(e))
    click.echo("\t'%s'" % (e.description))
    for q in e.equipment:
        click.echo("\t-> %u %s" % (q.id, q.name))

@exercise_cli.command("export")
def cli_exercise_export():
    export_dir = Path("exported")
    export_dir.mkdir(exist_ok=True)
    exercise_export_dir = export_dir / "exercises"
    exercise_export_dir.mkdir(exist_ok=True)
    count = export_models(ExerciseModel, ExerciseSchema, exercise_export_dir)
    click.echo("Exported {i} ExerciseModels.".format(i=count))


@exercise_cli.command("import")
def cli_exercise_import():
    import_dir = Path("imported")
    exercise_import_dir = import_dir / "exercises"
    count = import_models(ExerciseModel, ExerciseSchema,\
        exercise_import_dir, db.session)
    click.echo("Imported {i} ExerciseModels.".format(i=count))
