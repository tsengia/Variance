from pathlib import Path
import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.nutrition import NutrientInfoModel
from variance.schemas.nutrition import NutrientInfoSchema

from variance.common.json_export import export_models

nutrient_cli = AppGroup("nutrient")
nutrient_mod_cli = AppGroup("mod")
nutrient_cli.add_command(nutrient_mod_cli)


@nutrient_cli.command("list")
def cli_nutrient_list():
    n_list = NutrientInfoModel.query.all()
    if n_list is None:
        click.echo("NutrientInfo list is empty!")
        return -1
    for n in n_list:
        click.echo(str(n))


@nutrient_cli.command("view")
@click.argument("id")
def cli_nutrient_view(id):
    n = NutrientInfoModel.query.get(id)
    if n is None:
        click.echo("Could not find an nutrient with that ID!")
        return -1
    click.echo(str(n))

@nutrient_cli.command("export")
def cli_nutrient_export():
    export_dir = Path("exported")
    export_dir.mkdir(exist_ok=True)
    nutrient_export_dir = export_dir / "nutrients"
    nutrient_export_dir.mkdir(exist_ok=True)
    export_models(NutrientInfoModel, NutrientInfoSchema, nutrient_export_dir)
