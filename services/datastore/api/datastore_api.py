"""Flask REST API App.

This script does the setup and configuration for the Flask webapp, including
retrieving the configuration class from config.py, setting up the Postgres
connection for SQLAlchemy, the Datastore Model, and Datastore Controller.
"""
import uuid
from datetime import datetime

from flask import jsonify, make_response, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

# from database import db, ma
from datastore.database import db
from datastore.models.datastore_model import (
    DatastoreModel,
    datastore_schema,
    datastore_schemas,
)
from datastore.utility import strtobool


class DatastoreController(Resource):
    """flask-restful Controller for the Datastore."""

    def get(self, datastore_id: int = -1):
        """Read a Datastore entry by it's ID, or return all Datastore entries, as JSON."""
        data = {}
        # if a datastore_id isn't supplied, return all entries
        if datastore_id == -1:
            results = DatastoreModel.query.all()
            # ensure we have results
            if not results:
                return make_response(
                    jsonify(message="No datastore data has been created."), 404
                )
            data = datastore_schemas.dump(results)
        else:
            # Attempt to retrieve the Datastore entry, or fail with an HTTP 404.
            # A generic 404 message is used to prevent enumeration attacks.
            # https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
            # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#flask_sqlalchemy.SQLAlchemy.get_or_404
            results = db.get_or_404(DatastoreModel, datastore_id)
            data = datastore_schema.dump(results)
        return jsonify(data)

    def get_json_data(self):
        """Attempt to read the JSON data."""
        # read the JSON data
        email = request.json.get("email", "")
        uuid = request.json.get("uuid", "")
        bool = request.json.get("bool", "")
        datetime = request.json.get("datetime", "")

        return {
            "email": email,
            "uuid": uuid,
            "bool": bool,
            "datetime": datetime,
        }

    def post(self):
        """Create a new Datastore entry."""
        # read the JSON data, and pass it to the init function using kwargs
        datastore_entry = DatastoreModel(**self.get_json_data())
        # datastore_entry = datastore_schema.load(self.get_json_data())
        db.session.add(datastore_entry)
        try:
            db.session.commit()
        except IntegrityError:
            # https://docs-sqlalchemy.readthedocs.io/ko/latest/core/exceptions.html
            return make_response(
                jsonify(message="The email and UUID need to be unique."), 404
            )

        # return as JSON
        return make_response(jsonify(datastore_schema.dump(datastore_entry)), 201)

    def put(self, datastore_id: int = -1):
        """Update an existing Datastore entry."""
        # ensure we have a valid datastore_id
        if datastore_id == -1:
            return make_response(
                jsonify(message="Invalid datastore_id, it must be an int number."), 404
            )

        # attempt to get the existing Datastore entry, or return an HTTP 404
        datastore_entry = db.get_or_404(DatastoreModel, datastore_id)

        # read the JSON data, update the DatastoreModel
        json = self.get_json_data()
        datastore_entry.email = json["email"]
        datastore_entry.uuid = uuid.UUID(json["uuid"])
        datastore_entry.bool = strtobool(json["bool"])
        datastore_entry.datetime = datetime.strptime(
            json["datetime"], "%Y-%m-%dT%H:%M:%S.%f"
        )

        try:
            # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#updating-orm-objects-using-the-unit-of-work-pattern
            db.session.commit()
        except IntegrityError:
            # https://docs-sqlalchemy.readthedocs.io/ko/latest/core/exceptions.html
            return make_response(
                jsonify(message="The email and UUID need to be unique."), 404
            )
        return datastore_schema.jsonify(datastore_entry)

    def delete(self, datastore_id: int = -1):
        """Delete a Datastore entry."""
        # ensure we have a valid datastore_id
        if datastore_id == -1:
            return make_response(
                jsonify(message="Invalid datastore_id, it must be an int number."), 404
            )
        # attempt to retrieve a Datastore entry by it's datastore_id, or return a 404
        data = db.get_or_404(DatastoreModel, datastore_id)
        db.session.delete(data)
        db.session.commit()
        # jsonify(datastore_schema.dump(data))
        return jsonify({})


# https://flask.palletsprojects.com/en/2.3.x/api/#flask.Flask.add_url_rule
# @app.route("/aggregate")
def aggregate():
    """Call an ad-hoc text SQL query."""
    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#query-the-data
    # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute
    results = db.session.execute(
        text("SELECT COUNT(*) AS total FROM datastore;")
    ).fetchall()
    return jsonify(message=str(results))


# https://flask.palletsprojects.com/en/2.3.x/api/#flask.Flask.add_url_rule
# @app.route("/")
def hello_world():
    """Verify that Flask is running."""
    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#query-the-data
    return jsonify(hello="world")
