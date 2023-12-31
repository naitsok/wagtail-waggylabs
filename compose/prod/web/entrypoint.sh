#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

postgres_ready() {
python << END
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname="${DJANGO_SQL_DATABASE}",
        user="${DJANGO_SQL_USER}",
        password="${DJANGO_SQL_PASSWORD}",
        host="${DJANGO_SQL_HOST}",
        port="${DJANGO_SQL_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
seconds=30
until postgres_ready || [ $seconds -eq 0 ]; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
  ((seconds--))
done
if [ $seconds = 0 ]; then
	>&2 echo 'PostgreSQL is unavailable'
else
	>&2 echo 'PostgreSQL is available'
fi


exec "$@"