"""Utility script to configure the Flask App."""
import os


# https://flask.palletsprojects.com/en/2.3.x/config/
# https://flask.palletsprojects.com/en/2.3.x/api/#flask.Config.from_object
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/
class Config(object):
    """Configuration class for the Flask App."""

    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/#flask_sqlalchemy.config.SQLALCHEMY_DATABASE_URI
    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/#connection-url-format
    # https://docs.sqlalchemy.org/en/20/core/engines.html#postgresql
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://")

    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/#flask_sqlalchemy.config.SQLALCHEMY_TRACK_MODIFICATIONS
    # If enabled, all insert, update, and delete operations on models are
    # recorded, then sent in models_committed and before_models_committed
    # signals when session.commit() is called. This adds a significant amount
    # of overhead to every session.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
