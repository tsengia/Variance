from datetime import datetime

import click
from flask.cli import AppGroup

from variance import db
from variance.models.user import UserModel

user_cli = AppGroup("user")
user_mod_cli = AppGroup("mod")
user_cli.add_command(user_mod_cli)


@user_cli.command("get")
@click.argument("username")
def cli_user_get(username):
    u = UserModel.query.filter_by(username=username).first()
    if u is None:
        click.echo("No user with that username found!")
        return -1
    click.echo("User ID: %u" % u.id)


@user_cli.command("list")
def cli_user_list():
    u_list = UserModel.query.all()
    if u_list is None:
        click.echo("User list is empty!")
        return -1
    for u in u_list:
        click.echo("%u : %s, Role: %s, Created: %s, Birthday: %s" % (
            u.id, u.username, u.role, str(u.created_on), str(u.birthdate)))


@user_cli.command("add")
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


@user_cli.command("del")
@click.argument("user_id")
def cli_user_del(user_id):
    u = UserModel.query.get(user_id)
    if u is None:
        click.echo("No user with that ID found!")
        return -1
    name = str(u)
    db.session.delete(u)
    db.session.commit()
    click.echo("User %u (%s) deleted." % (user_id, name))


@user_cli.command("view")
@click.argument("user_id")
def cli_user_del(user_id):
    u = UserModel.query.get(user_id)
    if u is None:
        click.echo("No user with that ID found!")
        return -1
    click.echo("User %u (%s):" % (u.id, u.username))
    click.echo("\tRole: %s" % (u.role))
    click.echo("\tBirthday: %s" % (u.birthdate))
    click.echo("\tCreated on: %s" % (u.created_on))
    click.echo("\tEmail: %s" % (u.email))
    click.echo("\tTags: %s" % (str(u.get_tags())))


@user_mod_cli.command("role")
@click.argument("user_id")
@click.argument("new_role")
def cli_user_mod_role(user_id, new_role):
    u = UserModel.query.get(user_id)
    if u is None:
        click.echo("No user with that ID found!")
        return -1
    u.role = new_role
    db.session.commit()
    click.echo("User %u (%s) role update to %s." %
               (int(user_id), str(u.username), new_role))
