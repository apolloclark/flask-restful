"""Flask Application Factory function definition for create_app()."""
from flask import Flask
from flask_restful import Api

from datastore.api.datastore_api import DatastoreController, aggregate, hello_world
from datastore.database import db, ma
from datastore.models.datastore_model import DatastoreModel


# https://flask.palletsprojects.com/en/2.3.x/tutorial/factory/
# https://gitlab.com/patkennedy79/flask_user_management_example/-/blob/main/project/__init__.py
def create_app():
    """Flask Application Factory function to initialize the app."""
    # configure and initialize Flask
    app = Flask(__name__)
    app.config.from_object("datastore.config.Config")
    app.url_map.strict_slashes = False
    app.add_url_rule("/", view_func=hello_world)
    app.add_url_rule("/aggregate", view_func=aggregate)

    # initialize SQLAlchemy and Marshmallow
    db.init_app(app)
    ma.init_app(app)

    # initialize and configure flask-restful
    api = Api(app)
    api.add_resource(DatastoreController, "/datastore")
    api.add_resource(
        DatastoreController, "/datastore/<int:datastore_id>", endpoint="datastore"
    )
    return app


def app_reset_db():
    """Reset the database by dropping all tables and then creating them."""
    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#flask_sqlalchemy.SQLAlchemy.drop_all
    db.drop_all()
    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#flask_sqlalchemy.SQLAlchemy.create_all
    db.create_all()
    # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit
    db.session.commit()


def app_seed_db():
    """Seed the "datastore" table with data."""
    # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add
    db.session.add(DatastoreModel(email="apolloclark@gmail.com"))
    db.session.add(DatastoreModel(email="tom.jones@gmail.com"))
    db.session.add(
        DatastoreModel(
            email="wayland.yutani@gmail.com",
            uuid="752346e1-df66-485e-8f49-eb749d9ab666",
            bool="true",
            datetime="2023-07-25T16:58:36.908339",
        )
    )
    db.session.add(
        DatastoreModel(
            email="rick.deckard@gmail.com",
            uuid="752346e1-df66-485e-8f49-eb749d9ab806",
            bool="false",
            datetime="2023-07-25T16:57:36.908339",
        )
    )
    db.session.commit()
