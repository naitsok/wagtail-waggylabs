#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate --noinput
# python manage.py collectstatic --clear --noinput
# permissions for static and media files fixed
python manage.py collectstatic --noinput
python manage.py createsuperuser_container
# python manage.py runserver 0.0.0.0:8000
gunicorn waggylabs_site.wsgi:application --bind 0.0.0.0:8000