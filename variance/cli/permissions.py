import click
from flask.cli import AppGroup

from variance import db
from variance.models.permissions import PermissionModel

permissions_cli = AppGroup("perm")
permissions_mod_cli = AppGroup("mod")
permissions_cli.add_command(permissions_mod_cli)

@permissions_cli.command("get_action")
@click.argument("action")
def cli_permission_get_by_action(action):
    p = PermissionModel.query.filter_by(action=action)
    if p is None:
        click.echo("No permissions with that action type found!")
        return -1
    for i in p:
        click.echo(str(i))
        
@permissions_cli.command("list")
def cli_permission_list():
    p = PermissionModel.query.all()
    for i in p:
        click.echo(str(i))
        
        
@permissions_cli.command("del")
@click.argument("perm_id")
def cli_permission_del(perm_id):
    p = PermissionModel.query.get(perm_id)
    if p is None:
        click.echo("No permission with that ID found!")
        return -1
    action = p.action
    db.session.delete(p)
    db.session.commit()
    click.echo("Permission %u (%s) deleted." % (int(p.id), action))
    
@permissions_cli.command("add")
@click.argument("action")
@click.option("-r","--role","r", type=str)
@click.option("-u","--allow-uid","u", type=int)
@click.option("-o","--allow-owner","o", is_flag=True)
@click.option("-cp","--check-public","cp", is_flag=True)
@click.option("-fp","--force-public","fp", is_flag=True)
def cli_permission_add(action,r,u,o,cp,fp):
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