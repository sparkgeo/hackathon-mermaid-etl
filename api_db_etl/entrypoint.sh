#!/bin/sh

set -e

touch /status/schema/awaiting-upgrade

until python -m app.database_check
do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "Applying alembic migrations"
alembic -c /app/migrations/alembic.ini upgrade head

rm /status/schema/awaiting-upgrade

exec "$@"
