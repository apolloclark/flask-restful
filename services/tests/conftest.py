"""Pytest base class"""
import pytest

from datastore.app import app_reset_db, app_seed_db, create_app


# https://flask.palletsprojects.com/en/2.3.x/testing/
# https://gitlab.com/patkennedy79/flask_user_management_example/-/blob/main/tests/conftest.py
@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app

# https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture(scope='module')
def test_client(app):
    flask_app = create_app()
    flask_app.config.update({"TESTING": True})

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens

            # https://xvrdm.github.io/2017/07/03/testing-flask-sqlalchemy-database-with-pytest/


@pytest.fixture(scope='module')
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope='module')
def init_database(test_client):
    print("init_database()")
    app_reset_db()
    app_seed_db()
