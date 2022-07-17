import click
from flask.cli import AppGroup

from variance.extensions import db
from variance.models.permissions import PermissionModel
from variance.schemas.permissions import PermissionSchema
from variance.cli.resource import ResourceCLI

permissions_cli = ResourceCLI(PermissionModel, PermissionSchema, "Permissions", "perms", ("id",))
permissions_mod_cli = AppGroup("mod")
permissions_cli.group.add_command(permissions_mod_cli)

@permissions_cli.group.command("get_action")
@click.argument("action")
def cli_permission_get_by_action(action):
    p = PermissionModel.query.filter_by(action=action)
    if p is None:
        click.echo("No permissions with that action type found!")
        return -1
    for i in p:
        click.echo(str(i))

@permissions_cli.group.command("add")
@click.argument("action")
@click.option("-r", "--role", "r", type=str)
@click.option("-u", "--allow-uid", "u", type=int)
@click.option("-o", "--allow-owner", "o", is_flag=True)
@click.option("-cp", "--check-public", "cp", is_flag=True)
@click.option("-fp", "--force-public", "fp", is_flag=True)
def cli_permission_add(action, r, u, o, cp, fp):
    p = PermissionModel(action=action)

    if r:
        p.allow_role = r
    if u:
        p.allow_user = u
    if o:
        p.allow_owner = o
    if cp:
        p.check_public = cp
    if fp:
        p.force_public = fp

    db.session.add(p)
    db.session.commit()
    click.echo("Permission added for action %s." % (action))
