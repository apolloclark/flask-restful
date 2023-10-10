"""Datastore Model and Schema classes."""
import uuid as uuid_util
from datetime import datetime as datetime_util

from datastore.database import db, ma
from datastore.utility import strtobool


# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/models/
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
class DatastoreModel(db.Model):
    """Datastore, SQLAlchemy Database Model class.

    Attributes
    ----------
    datastore_id : int
        a globally unique ID for the each entry
    email : string
        user's email address
    uuid : uuid
        uuid for each entry
    bool : bool
        classic Boolean
    datetime : DateTime
        date and time of the entries creation

    Methods
    -------
    __init__(self, email="test@gmail.com")
    """

    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#flask_sqlalchemy.model.Model.__tablename__
    __tablename__ = "datastore"

    # https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column
    # https://docs.sqlalchemy.org/en/20/core/type_basics.html#generic-camelcase-types
    # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
    datastore_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    uuid = db.Column(db.Uuid(), unique=True, nullable=False)
    bool = db.Column(db.Boolean(), default=True, nullable=True)
    datetime = db.Column(db.DateTime(), nullable=True, server_default=db.func.now())

    def __init__(
        self,
        email: str = "",
        uuid: str = "",
        bool: str = "false",
        datetime: str = "",
    ):
        """Initialize the Datastore Model."""
        self.email = email

        # create a new random UUID if one is not given
        if not uuid:
            self.uuid = uuid_util.uuid4()
        else:
            self.uuid = uuid_util.UUID(uuid)

        # type cast the String to a Boolean
        self.bool = strtobool(bool)

        if datetime:
            self.datetime = datetime_util.strptime(datetime, "%Y-%m-%dT%H:%M:%S.%f")


# https://marshmallow.readthedocs.io/en/stable/marshmallow.schema.html
class DatastoreSchema(ma.Schema):
    """Datastore, Flask-Marshmallow Schema class, which wraps the SQLAlchemy Model."""

    class Meta:
        """Flask-Marshmallow Meta Schema class to configure the DatastoreSchema class."""

        model = DatastoreModel
        fields = ("datastore_id", "email", "uuid", "bool", "datetime", "_links")


datastore_schema = DatastoreSchema()
datastore_schemas = DatastoreSchema(many=True)  # note the plural variable name
