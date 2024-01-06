# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim-buster as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install system packages required by Wagtail and Django.
# https://github.com/wagtail/wagtail/blob/main/wagtail/project_template/Dockerfile
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./compose/dev/entrypoint.sh ./entrypoint.sh
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

COPY ./compose/dev/start.sh ./start.sh
RUN sed -i 's/\r$//g' ./start.sh
RUN chmod +x ./start.sh

# Copy the source code into the container.
COPY ./waggylabs ./waggylabs
COPY ./waggylabs_site ./waggylabs_site
COPY ./manage.py ./manage.py

# Expose the port that the application listens on.
EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

# Run the application.
# CMD gunicorn 'waggylabs_site.wsgi' --bind=0.0.0.0:8000
