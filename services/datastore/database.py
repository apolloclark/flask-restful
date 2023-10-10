"""SQLAlchemy database connection and Marshmallow Serialization object."""
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()
