import click
from flask.cli import AppGroup

from variance import db
from variance.models.muscle import MuscleModel, MuscleGroupModel

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
