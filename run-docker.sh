#!/usr/bin/env bash

# https://docs.docker.com/compose/gettingstarted/

# shutdown any running containers defined in the docker-compose.yml file
# and delete any volumes, including the persistent data from Postgres
docker compose down -v # https://docs.docker.com/engine/reference/commandline/compose_down/

# rebuild the Docker containers
docker compose build # https://docs.docker.com/engine/reference/commandline/compose_build/

# startup the Containers
docker compose up -d # https://docs.docker.com/engine/reference/commandline/compose_up/

# start streaming the container logs to the CLI
docker compose logs -f # https://docs.docker.com/engine/reference/commandline/compose_logs/
