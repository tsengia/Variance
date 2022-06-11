import click
from flask.cli import AppGroup
from variance.extensions import db

from sqlalchemy import text

db_cli = AppGroup("db")


@db_cli.command("drop-all")
def cli_db_drop_all():
    click.echo("Dropping all tables from database...")
    db.drop_all()
    click.echo("All tables dropped.")


@db_cli.command("init")
def cli_db_init():
    click.echo("Initializing database...")
    db.create_all()
    click.echo("Database initialized.")

@db_cli.command("prompt")
def cli_db_prompt():
    click.echo("Entering Database interactive prompt, be careful!")
    done = False
    with db.session() as s:
        try:
            while not done:
                cmd = click.prompt("VDB")
                if (cmd.lower() == "quit" or cmd.lower() == "exit"):
                    done = True
                    break 
                elif (cmd.lower() == "commit"):
                    s.commit()
                elif cmd.lower() == "rollback":
                    s.rollback()
                else:
                    res = s.execute(text(cmd))
                    rows = res.all()
                    click.echo("Command returned {i} rows.".format(i=len(rows)))
                    if len(rows) > 0:
                        key_string = "Keys: "
                        keys = res.keys()
                        for k in keys:
                            key_string += k + ", "
                        click.echo(key_string)
                    for r in rows:
                        click.echo(str(r).replace("(","").replace(")",""))
        except Exception as e:
            click.echo("Exception caught, rollingback and exiting!")
            click.echo("Exception: " + str(e))
            s.rollback()
    
    click.echo("Exited Database interactive prompt.")
