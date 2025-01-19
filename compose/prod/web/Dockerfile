# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12

###########
# BUILDER #
###########

# pull official base image
FROM python:${PYTHON_VERSION}-slim-bookworm as builder

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# lint
# RUN pip install flake8==6.1.0
# COPY ./waggylabs ./waggylabs
# COPY ./waggylabs_site ./waggylabs_site
# COPY ./manage.py ./manage.py
# RUN flake8 --ignore=E501,F401 .

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


#########
# FINAL #
#########

FROM python:${PYTHON_VERSION}-slim-bookworm as base

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# Install system packages required by Wagtail and Django.
# https://github.com/wagtail/wagtail/blob/main/wagtail/project_template/Dockerfile
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.prod.sh
COPY ./compose/prod/web/entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy entrypoint.prod.sh
COPY ./compose/prod/web/start.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/start.sh
RUN chmod +x  $APP_HOME/start.sh

# copy project
COPY ./waggylabs ./waggylabs
COPY ./waggylabs_site ./waggylabs_site
COPY ./manage.py ./manage.py

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
