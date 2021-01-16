import click
from flask.cli import AppGroup
from variance import db

lf_cli = AppGroup("load-fixture")

@lf_cli.command("units")
def cli_fixture_load_units():
    click.echo("Adding default units...")
    from variance.fixtures.units import DEFAULT_UNITS
    from variance.models.unit import UnitModel
    
    # By default all fixture units are not removable. Aka they are not created by a user
    for u in DEFAULT_UNITS:
        m = UnitModel(multiplier=u[0], name=u[1][-1], dimension=u[2], abbreviation=u[1][0], removable=False)
        db.session.add(m)
        db.session.commit()
    click.echo("Default units added.")
    
@lf_cli.command("equipment")
def cli_fixture_load_equipment():
    click.echo("Adding default equipment...")
    from variance.fixtures.equipment import DEFAULT_EQUIPMENT
    from variance.models.equipment import EquipmentModel
    
    for e in DEFAULT_EQUIPMENT:
        m = EquipmentModel(name=e[0], description=e[1])
        db.session.add(m)
        db.session.commit()
    click.echo("Default equipment added.")
    
@lf_cli.command("muscles")
def cli_fixture_load_muscles():
    click.echo("Adding default muscles...")
    from variance.fixtures.muscles import DEFAULT_MUSCLES, DEFAULT_MUSCLE_GROUPS
    from variance.models.muscle import MuscleModel, MuscleGroupModel
    
    for e in DEFAULT_MUSCLE_GROUPS:
        m = MuscleGroupModel(name=e[0], description=e[1])
        db.session.add(m)
        db.session.commit()
    
    for e in DEFAULT_MUSCLES:
        short_name = e[1]
        if len(short_name) == 0:
            short_name = e[0]
        m = MuscleModel(name=e[0], short_name=short_name, diagram_id=e[3])
        db.session.add(m)
        for g in e[2]:
            m.groups.append(MuscleGroupModel.query.get(g))
        db.session.commit()
    click.echo("Default muscles and muscle groups added.")