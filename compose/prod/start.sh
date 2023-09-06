#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate --noinput
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py createsuperuser_container
python manage.py runserver 0.0.0.0:8000