from pathlib import Path

import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.unit import UnitModel
from variance.schemas.unit import UnitSchema

from variance.models.muscle import MuscleModel
from variance.schemas.muscle import MuscleSchema

from variance.models.nutrition import NutrientInfoModel, ConsumableModel, RecipeModel
from variance.schemas.nutrition import NutrientInfoSchema, ConsumableSchema, RecipeSchema

from variance.models.equipment import EquipmentModel
from variance.schemas.equipment import EquipmentSchema

from variance.models.exercise import ExerciseModel
from variance.schemas.exercise import ExerciseSchema

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
        unit_file.write_text(unit_dump_schema.dumps(u))

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
        muscle_file.write_text(muscle_dump_schema.dumps(m))

@export_cli.command("nutrients")
def cli_export_list():
    n_list = NutrientInfoModel.query.all()
    if n_list is None:
        click.echo("NutrientInfo list is empty!")
        return -1
    export_dir = Path("exported")
    export_dir.mkdir(exist_ok=True)
    nutrient_export_dir = export_dir / "nutrients"
    nutrient_export_dir.mkdir()
    nutrient_dump_schema = NutrientInfoSchema(exclude=("id",))
    for n in n_list:
        cname = n.canonical_name
        nutrient_file = nutrient_export_dir / (cname + ".json")
        nutrient_file.write_text(nutrient_dump_schema.dumps(n))

@export_cli.command("exercises")
def cli_export_list():
    e_list = ExerciseModel.query.all()
    if e_list is None:
        click.echo("Exercise list is empty!")
        return -1
    export_dir = Path("exported")
    export_dir.mkdir(exist_ok=True)
    exercise_export_dir = export_dir / "exercises"
    exercise_export_dir.mkdir()
    exercise_dump_schema = ExerciseSchema(exclude=("id",))
    for e in e_list:
        cname = e.canonical_name
        exercise_file = exercise_export_dir / (cname + ".json")
        exercise_file.write_text(exercise_dump_schema.dumps(e))
