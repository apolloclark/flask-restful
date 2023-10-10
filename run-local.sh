#!/usr/bin/env bash

export FLASK_APP=project/__init__.py
export FLASK_RUN_PORT=5001
cd ./services/web
python3 manage.py run
