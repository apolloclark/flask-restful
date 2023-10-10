#!/bin/sh

# ensure we have a Postgres database connection available
if [ "$DATABASE" = "postgres" ]
then
    echo "[INFO] Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "[INFO] PostgreSQL started."
fi

echo "[INFO] Initializing the database."
python cli.py reset_db

exec "$@"
