# pull official base image
FROM python:3.10.6-slim-buster

# set work directory
# https://docs.docker.com/engine/reference/builder/#workdir
WORKDIR /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 # Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1 # Prevents Python from buffering stdout and stderr

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./datastore/requirements.txt /usr/src/app/datastore/requirements.txt
RUN pip install -r ./datastore/requirements.txt

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
