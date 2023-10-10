"""Utility script to provide a CLI for the Flask app."""
from flask.cli import FlaskGroup

from datastore.app import app_reset_db, app_seed_db, create_app, db
from datastore.models.datastore_model import DatastoreModel


# https://flask.palletsprojects.com/en/2.3.x/api/#flask.cli.FlaskGroup
# https://pocoo-click.readthedocs.io/en/latest/advanced/#invoking-other-commands
cli = FlaskGroup(create_app=create_app)

@cli.command("reset_db")
def reset_db():
    """Reset the database."""
    app_reset_db()


@cli.command("seed_db")
def seed_db():
    """Seed the database with testing data."""
    app_seed_db()


@cli.command("reinit_db")
def reinit_db():
    """Reset and then seed the database."""
    app_reset_db()
    app_seed_db()


if __name__ == "__main__":
    cli()
