import click
from flask.cli import AppGroup

from variance import db
from variance.models.muscle import MuscleModel, MuscleGroupModel

muscle_cli = AppGroup("muscle")
muscle_mod_cli = AppGroup("mod")
muscle_cli.add_command(muscle_mod_cli)
    
@muscle_cli.command("list")
def cli_muscle_list():
    m_list = MuscleModel.query.all()
    if m_list is None:
        click.echo("Muscle list is empty!")
        return -1
    for m in m_list:
        click.echo(str(m))