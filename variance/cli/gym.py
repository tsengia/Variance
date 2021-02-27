import click
from flask.cli import AppGroup

from variance import db
from variance.models.gym import GymModel
from variance.models.equipment import EquipmentModel

gym_cli = AppGroup("gym")
gym_mod_cli = AppGroup("mod")
gym_cli.add_command(gym_mod_cli)

@gym_cli.command("list")
def cli_gym_list():
    g_list = GymModel.query.all()
    if g_list is None:
        click.echo("Gym list is empty!")
        return -1
    for g in g_list:
        click.echo(str(g))