# flask-restful

This is a demo project using the Python Flask framework to create a REST API
with a Postgres database running within a Docker environment, along with
flask-restul, SQLAlchemy, flask-sqlalchemy, Marshmallow, flask-marshmallow,
marshmallow-sqlalchemy, and flake8.

In an Enterprise quality application, Business Scenarios needs to be defined,
translated into a high-level User Stories, then into a Acceptance Criteria in the
form of Given-When-Then Scenarios, then into specific Use Cases, the collection
of which is an Epic. The Use Cases are translated into Behavior Driven
Development (BDD) scenarios that are validated by End-to-End Tests (e2e),
Functional Tests, and Unit Tests, using Stubs and Mocks to increase speed.

- https://www.altexsoft.com/blog/business/acceptance-criteria-purposes-formats-and-best-practices/
- https://hypothesis.readthedocs.io/en/latest/
- https://pypi.org/project/hypothesis/
- https://pynguin.readthedocs.io/en/latest/user/intro.html
- https://pypi.org/project/pytest-automock/
- https://github.com/pksol/mock_autogen
- https://github.com/pytest-dev/pytest-randomly
- https://pytest-bdd.readthedocs.io/en/latest/

- https://pypi.org/project/pytest-flask-sqlalchemy/
- https://medium.com/@aswens0276/using-pytest-to-setup-dynamic-testing-for-your-flask-apps-postgres-database-locally-and-with-39a14c3dc421
- http://alexmic.net/flask-sqlalchemy-pytest/
- https://bytes.yingw787.com/posts/2021/02/02/property_based_testing/




## TODO
- Add Unittests
  - https://ericbernier.com/flask-restful-api
  - https://dev.to/nahidsaikat/flask-with-sqlalchemy-marshmallow-5aj2
  - https://flask.palletsprojects.com/en/2.3.x/testing/
  - https://docs.pytest.org/en/latest/
  - https://github.com/pallets/flask/tree/1.1.4/examples/tutorial
  - https://github.com/ericmbernier/ericbernier-blog-posts/tree/master/flask_rest_api
  - https://testdriven.io/blog/flask-pytest/
  - https://gitlab.com/patkennedy79/flask_user_management_example/-/tree/main
- Add automated edge-case testing
  1. (null)
  2. lower-bound
  3. upper-bound
  4. under-flow
  5. over-flow
  6. non-unique value
  7. missing entity
  8. type mismatch
  9. malformed
  10. missing keys
  11. null values
  12. Unicode
  13. XSS
  14. SQL/NoSQL injection
- Add Flask Blueprints, for Modules
- Add Terraform to deploy
  - AWS, EC2
  - Azure, VM
  - GCP, Compute
  - K3S
  - AWS, ECS
  - AWS, EKS
  - AWS Lambda
- Add HashiCorp Vault for Secrets Management
- Add multiple output data formats
  - https://flask-restful.readthedocs.io/en/latest/extending.html#resource-method-decorators
- Add multiple input data formats
- Add RBAC security controls
  - https://www.aserto.com/blog/flask-rbac-demystified-a-developer-s-guide
  - https://flask-rbac.readthedocs.io/en/latest/
  - https://flask-authorize.readthedocs.io/en/latest/
  - https://mikeboers.github.io/Flask-ACL/
- Add flask-statds for metrics
- Add logging
  - https://flask.palletsprojects.com/en/2.3.x/logging/
- Add flask-sqlalchemy, backup, restore
  - https://pypi.org/project/flask-alchemydumps/
- Add read-only maintenance mode
- Add multi-region fail-over
- Add MariaDB, Redis, Memcached, ElasticSearch, MongoDB, Kafka, Neo4J
- Add automated upgrades
- Add multi-region support




## Getting Started

```sh
git clone
cd ./flask-restful

# run using Docker
./run-docker.sh

# debug with Docker

## shutdown any running containers defined in the docker-compose.yml file
## and delete any volumes, including the persistent data from Postgres
docker compose down -v # https://docs.docker.com/engine/reference/commandline/compose_down/

# rebuild the Docker containers
docker compose build # https://docs.docker.com/engine/reference/commandline/compose_build/

# startup the Containers
docker compose up -d # https://docs.docker.com/engine/reference/commandline/compose_up/

## list any running Docker containers
## https://docs.docker.com/engine/reference/commandline/compose_down/
docker compose ls

## get the Docker container logs
## https://docs.docker.com/engine/reference/commandline/compose_logs/
docker compose logs -f

## rebuild the Postgres database tables
docker compose exec web python cli.py reset_db

## test that the database table was created
docker compose exec db psql --username=hello_flask --dbname=hello_flask_dev

### list the available databases
> \l

### connect to the database
> \c hello_flask_dev

### list the tables
> \dt

List of relations
Schema | Name  | Type  |    Owner    
--------+-------+-------+-------------
public | datastore | table | hello_flask
(1 row)

### disconnect
> \q

## verify the Postgres volume was created
docker volume inspect $(basename $(pwd))_postgres_data



## create the database
docker compose exec web python cli.py reset_db

## seed the database
docker compose exec web python cli.py seed_db

## reset the database
docker compose exec web python cli.py reinit_db

## verify the database was seeded
docker compose exec db psql --username=hello_flask --dbname=hello_flask_dev

### print the contents of the "datastore" table
> SELECT * FROM datastore;

id |         email         |                 uuid                 | bool |          datetime          
----+-----------------------+--------------------------------------+------+----------------------------
 1 | apolloclark@gmail.com   | 4362275a-2cbe-4eb9-bc47-1e8e50184fc7 | t    | 2023-07-21 22:43:29.923174
 2 | tom.jones@gmail.com     | 65596a6a-4bb8-4e5d-8edf-0e1016660fb0 | t    | 2023-07-21 22:43:29.923174
(2 rows


### disconnect
> \q



# run just the Flask App on your local machine, without Postgres
./run-local.sh
```




## Links

## Tutorial
- https://github.com/testdrivenio/flask-on-docker
- https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

### Components
- linting, documentation
  - https://cjolowicz.github.io/posts/hypermodern-python-05-documentation/
  - https://www.kevinpeters.net/auto-formatters-for-python
  - Black
    - https://pypi.org/project/black/
    - https://github.com/psf/black
    - https://black.readthedocs.io/en/stable/
  - Flake8
    - https://github.com/PyCQA/flake8
  - https://github.com/pylint-dev/pylint
  - Pyre
    - https://github.com/facebook/pyre-check
    - https://pypi.org/project/pyre-check/
  - https://github.com/PyCQA/bandit
  - https://github.com/PyCQA/autoflake
  - https://github.com/asottile/pyupgrade
  - https://github.com/DanielNoord/pydocstringformatter
- Flask
  - https://github.com/pallets/flask
- flask-restful
  - https://github.com/flask-restful/flask-restful
  - https://flask-restful.readthedocs.io/en/latest/quickstart.html
  - https://flask-restful.readthedocs.io/en/latest/reqparse.html
  - https://auth0.com/blog/developing-restful-apis-with-python-and-flask/
  - https://blog.teclado.com/first-rest-api-flask-postgresql-python/
  - https://www.tinystacks.com/blog-post/flask-crud-api-with-postgres/
- Postgres
  - https://hub.docker.com/_/postgres/tags
  - Latest is "15.3-bookworm"
- flask-sqlalchemy
  - https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
  - https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/models/
  - https://www.attilatoth.dev/posts/flask-sqlalchemy-multiple-dbs/
  - https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/binds/
- marshmallow
  - https://dev.to/nahidsaikat/flask-with-sqlalchemy-marshmallow-5aj2
  - https://github.com/marshmallow-code/marshmallow-sqlalchemy
  - https://marshmallow.readthedocs.io/en/stable/examples.html#quotes-api-flask-sqlalchemy
  - https://realpython.com/flask-connexion-rest-api-part-2/
- flask-marshmallow
  - https://github.com/marshmallow-code/flask-marshmallow
  - https://flask-marshmallow.readthedocs.io/en/latest/
- marshmallow-sqlalchemy
  - https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
- blueprints
  - https://flask.palletsprojects.com/en/2.3.x/blueprints/
- testing
  - https://flask.palletsprojects.com/en/2.3.x/testing/
  - https://docs.pytest.org/en/latest/
