#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
# http://redsymbol.net/articles/unofficial-bash-strict-mode/

# https://www.jumpingrivers.com/blog/python-linting-guide/
# https://gitlab.com/patkennedy79/flask_user_management_example/-/blob/main/.gitlab-ci.yml

# format and lint
# https://black.readthedocs.io/en/stable/getting_started.html
# https://github.com/psf/black
echo "[INFO] Formatting code..."
docker compose exec web black ./datastore
# pylint ./services/web

# https://pycqa.github.io/isort/docs/configuration/options.html
# https://pycqa.github.io/isort/docs/configuration/profiles.html
echo -e '\n[INFO] Formatting Python imports ordering, with isort...'
docker compose exec web isort . --profile black --lines-after-imports 2

# code complexity, lint, and docstring linting
# https://flake8.pycqa.org/en/latest/
# https://github.com/pycqa/flake8
# https://pypi.org/project/flake8-docstrings/
# radon cc ./web/ -a -nc
# xenon --max-absolute B --max-modules A --max-average A
echo -e '\n[INFO] Checking code complexity, quality, and docstrings, with flake8...'
docker compose exec web flake8 --max-complexity=10 \
  --ignore=E501 \
  --docstring-convention=google \
  --max-function-length=30 \
  --doctests ./datastore || true

echo -e "\n[INFO] Checking for Python library dependency updates, with pip..."
# https://pip.pypa.io/en/stable/cli/pip_list/
docker compose exec web pip list --outdated --exclude packaging

echo -e '\n[INFO] Checking python library dependencies security, with safety...'
docker compose exec web safety check --output bare
# docker compose exec web safety check

echo -e '\n[INFO] Checking code security, with bandit...'
docker compose exec web bandit -r ./datastore

# unit test
# https://flask.palletsprojects.com/en/2.3.x/testing/
echo -e "\n[INFO] Resetting the database, and seeding test data..."
docker compose exec web python cli.py reinit_db

echo -e "\n[INFO] Running functional and unit tests, with pytest..."
docker compose exec web pytest tests

echo -e "\n[INFO] Checking test coverage..."
docker compose exec web python -m pytest --cov-report term-missing --cov=datastore

# https://pypi.org/project/wily/
