"""
Module containing CLI commands for managing the Variance database and resources
"""
from . import db
from . import user
from . import unit
from . import equipment
from . import gym
from . import muscle
from . import exercise
from . import nutrient
from . import consumable
from . import tracker
from . import setting

import click
from flask.cli import AppGroup

# List of click command groups that support import and export commands
resource_command_list = [\
    unit.unit_cli,
    muscle.muscle_cli,
    muscle.muscle_group_cli,
    equipment.equipment_cli,
    exercise.exercise_cli,
    nutrient.nutrient_cli,
    tracker.tracker_cli,
    consumable.consumable_cli,
    gym.gym_cli,
    setting.setting_cli
]

all_cli = AppGroup("all")

def export_all(export_root):
    for r in resource_command_list:
        r.export_data(export_root)

@all_cli.command("export")
@click.argument("export_root", type=click.Path(), required=True)
def export_all_cmd(export_root):
    "CLI command to export all resources to a directory"
    click.echo("Exporting all resources into " + export_root)
    export_all(export_root)
    click.echo("Export finished.")

def import_all(import_root):
    for r in resource_command_list:
        r.import_data(import_root)

@all_cli.command("import")
@click.argument("import_root", type=click.Path(exists=True, file_okay=False), required=True)
def import_all_cmd(import_root):
    "CLI command to import all resources from a directory"
    click.echo("Importing all resources from " + import_root)
    import_all(import_root)
    click.echo("Import finished.")

@all_cli.command("count")
def count_all_resources_cmd():
    "CLI command that lists a count of each resource type"
    click.echo("Resource Type\t\t\tCount")
    for r in resource_command_list:
        click.echo(r.resource_name_ + "\t\t\t" + str(r.count()))