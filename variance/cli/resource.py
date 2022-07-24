"""
Contains ResourceCLI, a class that implements common cli commands for managing a resource.
"""
from typing import Optional
from pathlib import Path
import click
from flask.cli import AppGroup

from variance.extensions import db

from variance.common.json_export import export_models
from variance.common.json_import import import_models

class ResourceCLI():
    "Base class for managing Models through the CLI. Removes boilerplate/repetative code."
    group: AppGroup

    def attach(self, parent_group):
        "Adds this collection of commands to the given group"
        parent_group.add_command(self.group)

    def __init__(self, model: object, schema: object, resource_name: str, group_name: str, exclude: Optional[tuple[str]] = ()):
        self.group = AppGroup(group_name)
        self.model_ = model
        self.schema_ = schema
        self.resource_name_ = resource_name 
        self.exclude_ = exclude

        @self.group.command("list")
        def cli_list():
            "Querys all of the models in the DB and prints them using str(model)"
            r_list = db.session.query(self.model_)
            if r_list is None:
                click.echo("No results.")
                return
            for r in r_list:
                click.echo(str(r))

        @self.group.command("find")
        @click.argument("field", type=str, required=True)
        @click.argument("value", type=str, required=True)
        def cli_search(field, value):
            "Searches for instances that have _field_ set to _value_"
            filter_dict = {}
            filter_dict[field] = value
            m_list = db.session.query(self.model_).filter_by(**filter_dict)
            if m_list is None:
                click.echo("No results.")
                return

            click.echo("")
            click.echo("Find Results:")
            for m in m_list:
                click.echo(str(m))
            click.echo("")
    

        @self.group.command("view")
        @click.argument("resource_id", type=int, required=True)
        def cli_view(resource_id):
            "Dumps the JSON representation of the given resource."
            m = self.model_.query.get(resource_id)
            if m is None:
                click.echo("Failed to find {r} with ID of {i}!".format(\
                    r=self.resource_name_, i=resource_id))
                return
            s = self.schema_()
            click.echo("Viewing {r} with ID of {i}".format(r=self.resource_name_, i=resource_id))
            click.echo(s.dumps(m))

        @self.group.command("export")
        @click.argument("export_root", type=click.Path(), required=True)
        def cli_export(export_root):
            "Exports all models in the DB into JSON files"
            click.echo("Exporting " + self.resource_name_ + "...")
            export_dir = Path(export_root)
            export_dir.mkdir(exist_ok=True)
            resource_export_dir = export_dir / resource_name 
            resource_export_dir.mkdir(exist_ok=True)
            count = export_models(self.model_, self.schema_, resource_export_dir, self.exclude_)
            click.echo("Exported {i} {r} models.".format(i=count, r=self.resource_name_))

        @self.group.command("import")
        @click.argument("import_root", type=click.Path(exists=True, file_okay=False), required=True)
        def cli_import(import_root):
            "Imports models from JSON data"
            click.echo("Importing " + self.resource_name_ + "...")
            import_dir = Path(import_root)
            resource_import_dir = import_dir / self.resource_name_
            count = import_models(self.model_, self.schema_,\
                resource_import_dir, db.session, self.exclude_)
            click.echo("Imported {i} {r}.".format(i=count, r=self.resource_name_))

        @self.group.command("drop")
        def cli_drop():
            "Deletes all models in the DB."
            if not click.confirm("Are you sure you want to drop all {r}?".format(r=self.resource_name_)):
                click.echo("Cancelled.")
                return
            click.echo("Dropping all " + self.resource_name_)
            for a in db.session.query(self.model_).all():
                db.session.delete(a)
            db.session.commit()
            click.echo("Deleted all " + self.resource_name_ + "!")

        @self.group.command("delete")
        @click.argument("resource_id", type=int, required=True)
        def cli_del(resource_id):
            "Deletes the resource with the given ID"
            m = self.model_.query.get(resource_id)
            if m is None:
                click.echo("Unable to find resource with that ID!")
                return
            db.session.delete(m)
            db.session.commit()
            click.echo("Deleted {r} with ID={i}".format(r=self.resource_name_, i=resource_id))
