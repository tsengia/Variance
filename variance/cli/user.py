from datetime import datetime

import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.user import UserModel
from variance.schemas.user import UserSchema
from variance.cli.resource import ResourceCLI

user_cli = ResourceCLI(UserModel, UserSchema, "Users", "users")
user_set_cli = AppGroup("set")
user_cli.group.add_command(user_set_cli)

@user_cli.group.command("add")
@click.argument("username")
@click.argument("password")
@click.argument("birthdate")
def cli_user_add(username, password, birthdate):
    u = UserModel.query.filter_by(username=username).first()
    if u is not None:
        click.echo("A user with that username already exists!")
        return -1
    try:
        birthdate = datetime.fromisoformat(birthdate)
    except ValueError:
        click.echo("Birthdate must be in YYYY-MM-DD format!")
        return -1
    new_user = UserModel(username=username, birthdate=birthdate)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    click.echo("User %s added." % (username))


@user_set_cli.command("role")
@click.argument("user_uuid")
@click.argument("new_role")
def cli_user_mod_role(user_uuid, new_role):
    u = UserModel.query.get(user_uuid)
    if u is None:
        click.echo("No user with that UUID found!")
        return -1
    u.role = new_role
    db.session.commit()
    click.echo("User %s (%s) role update to %s." %
               (user_uuid, str(u.username), new_role))
