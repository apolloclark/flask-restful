"""Datastore Controller Tests"""
# These tests are run in order, so initially the database will be reset with data,
# but we want to test it without data first, since this is helpful to new
# developers to see, so we reset the database without any data, test, then
# reseed the data for the rest of the tests.
import pytest

from datastore.app import app_reset_db, app_seed_db, create_app
from datastore.database import db, ma
from datastore.utility import strtobool


error_404 = b'{\n    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."\n}\n'

def test_root(test_client):
    response = test_client.get("/")
    print(response.data)
    assert response.status_code == 200
    assert b'{\n  "hello": "world"\n}\n' in response.data

def test_datastore_get_root_empty_without_slash(test_client):
    app_reset_db()
    response = test_client.get("/datastore")
    assert b'{\n  "message": "No datastore data has been created."\n}\n' in response.data
    assert response.status_code == 404

def test_datastore_get_root_empty_with_slash(test_client):
    response = test_client.get("/datastore/")
    assert b'{\n  "message": "No datastore data has been created."\n}\n' in response.data
    assert response.status_code == 404
    app_seed_db()

def test_datastore_get_missing_entity(test_client):
    response = test_client.get("/datastore/999")
    assert response.status_code == 404
    assert error_404 in response.data

def test_datastore_get_root_populated_with_slash(test_client):
    response = test_client.get("/datastore/")
    assert response.status_code == 200
    assert b'"email": "apolloclark@gmail.com"' in response.data



def test_datastore_post(test_client):
    response = test_client.post("/datastore", json={
        "email":"alex.murphy@gmail.com",
        "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a303",
        "bool":"false",
        "datetime":"2023-07-25T16:57:36.908339"
    })
    assert response.status_code == 201
    assert b'"email": "alex.murphy@gmail.com"' in response.data
    assert b'"uuid": "0446d5c1-36c4-42d3-b006-247fcaa8a303"' in response.data
    assert b'"bool": false' in response.data
    assert b'"datetime": "2023-07-25T16:57:36.908339"' in response.data

def test_datastore_post_read_root_with_slash(test_client):
    response = test_client.get("/datastore/")
    assert response.status_code == 200
    assert b'"email": "alex.murphy@gmail.com"' in response.data

def test_datastore_post_read_by_entity_id(test_client):
    response = test_client.get("/datastore/5")
    assert response.status_code == 200
    assert b'"email": "alex.murphy@gmail.com"' in response.data

def test_datastore_post_error_nonunique_email(test_client):
    response = test_client.post("/datastore", json={
        "email":"alex.murphy@gmail.com",
        "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a333",
        "bool":"true",
        "datetime":"2023-07-25T16:57:36.908339"
    })
    assert response.status_code == 404
    db.session.rollback()

def test_datastore_post_error_nonunique_uuid(test_client):
    response = test_client.post("/datastore", json={
        "email":"alex.murphy999@gmail.com",
        "uuid":"752346e1-df66-485e-8f49-eb749d9ab666",
        "bool":"true",
        "datetime":"2023-07-25T16:57:36.908339"
    })
    assert response.status_code == 404
    db.session.rollback()



def test_datastore_put(test_client):
    response = test_client.put("/datastore/5", json={
        "email":"alex.murphy999@gmail.com",
        "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a999",
        "bool":"false",
        "datetime":"2023-07-25T16:57:36.999999"
    })
    assert response.status_code == 200
    assert b'"email": "alex.murphy999@gmail.com"' in response.data
    assert b'"uuid": "0446d5c1-36c4-42d3-b006-247fcaa8a999"' in response.data
    assert b'"bool": false' in response.data
    assert b'"datetime": "2023-07-25T16:57:36.999999"' in response.data

def test_datastore_put_read_root_with_slash(test_client):
    response = test_client.get("/datastore/")
    assert response.status_code == 200
    assert b'"email": "alex.murphy999@gmail.com' in response.data

def test_datastore_put_read_by_entity_id(test_client):
    response = test_client.get("/datastore/5")
    assert response.status_code == 200
    assert b'"email": "alex.murphy999@gmail.com' in response.data

def test_datastore_put_error_nonunique_email(test_client):
    response = test_client.put("/datastore/5", json={
         "email":"apolloclark@gmail.com",
         "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a999",
         "bool":"true",
         "datetime":"2023-07-25T16:57:36.999999"
    })
    assert response.status_code == 404
    assert b'"The email and UUID need to be unique."' in response.data
    db.session.rollback()

def test_datastore_put_error_nonunique_uuid(test_client):
    response = test_client.put("/datastore/5", json={
         "email":"alex.murphy999@gmail.com",
         "uuid":"752346e1-df66-485e-8f49-eb749d9ab806",
         "bool":"false",
         "datetime":"2023-07-25T16:57:36.999999"
    })
    assert response.status_code == 404
    assert b'"The email and UUID need to be unique."' in response.data
    db.session.rollback()

def test_datastore_put_missing_entity(test_client):
    response = test_client.put("/datastore/999", json={
        "email":"alex.murphy999@gmail.com",
        "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a999",
        "bool":"false",
        "datetime":"2023-07-25T16:57:36.999999"
    })
    assert response.status_code == 404

def test_datastore_put_null_entity(test_client):
    response = test_client.put("/datastore/", json={
        "email":"alex.murphy999@gmail.com",
        "uuid":"0446d5c1-36c4-42d3-b006-247fcaa8a999",
        "bool":"false",
        "datetime":"2023-07-25T16:57:36.999999"
    })
    assert b'Invalid datastore_id, it must be an int number.' in response.data
    assert response.status_code == 404



def test_datastore_delete_existing_entity(test_client):
    response = test_client.delete("/datastore/1")
    assert response.status_code == 200
    assert b'{}' in response.data

def test_datastore_delete_missing_entity(test_client):
    response = test_client.delete("/datastore/999")
    assert response.status_code == 404
    assert error_404 in response.data

def test_datastore_delete_null_entity(test_client):
    response = test_client.delete("/datastore/")
    assert response.status_code == 404
    assert b'"Invalid datastore_id, it must be an int number."' in response.data

def test_datastore_delete_get_missing_entity(test_client):
    response = test_client.get("/datastore/1")
    assert response.status_code == 404
    assert error_404 in response.data



def test_aggregate(test_client):
    response = test_client.get("/aggregate")
    print(response.data)
    assert response.status_code == 200
    assert b'"message": "[(4,)]"' in response.data

def test_strtobool_error():
    with pytest.raises(ValueError):
        strtobool("error")
