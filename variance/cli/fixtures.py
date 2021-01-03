from pathlib import Path
import click
from flask.cli import AppGroup
from variance.db import get_db
from flask import current_app

fixtures_cli = AppGroup("fixtures")
load_fixtures_cli = AppGroup("load-default")
gen_fixtures_cli = AppGroup("gen-default")

@gen_fixtures_cli.command("units")
def cli_fixtures_units_generate():
    from variance.core.units import MassUnit, VolumeUnit, LengthUnit, EnergyUnit, TimeUnit, SpeedUnit

    click.echo("Generating add_default_units.sql....")
    db = get_db()
    with current_app.open_instance_resource(Path("fixtures/generated/scripts/add_default_units.sql"), "w") as sql:
        sql.write("INSERT INTO UnitIndex (name, abbreviation, dimension) VALUES\n")

        sql.write("--Mass\n")
        for u in MassUnit:
            sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

        sql.write("--Volume\n")
        for u in VolumeUnit:
            sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

        sql.write("--Length\n")
        for u in LengthUnit:
            sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

        sql.write("--Energy\n")
        for u in EnergyUnit:
            sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

        sql.write("--Time\n")
        for u in TimeUnit:
            sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

        sql.write("--Speed\n")
        for u in SpeedUnit:
            sql.write("('" + u.value[1][-1] + "','" + u.value[1][0] + "','" + u.value[2] + "'),\n")

        sql.write("('deleted unit', 'del', 'deleted');")
        sql.close()
    click.echo("add_default_units.sql generated.")

@load_fixtures_cli.command("units")
def cli_fixtures_units_load():
    db = get_db()
    click.echo("Loading default units from add_default_units.sql...")
    with current_app.open_instance_resource(Path("fixtures/generated/scripts/add_default_units.sql")) as sql:
        db.executescript(sql.read().decode("utf-8"))
    db.commit()
    click.echo("Units loaded.")

fixtures_cli.add_command(gen_fixtures_cli)    
fixtures_cli.add_command(load_fixtures_cli)