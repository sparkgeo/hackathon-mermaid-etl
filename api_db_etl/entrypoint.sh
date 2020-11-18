#!/bin/sh

set -e

touch /status/schema/awaiting-upgrade
touch /status/couchdb/awaiting-database

until python -m app.couchdb_check
do
  sleep 1
done

rm /status/couchdb/awaiting-database

until python -m app.database_check
do
  sleep 1
done
alembic -c /app/migrations/alembic.ini upgrade head

rm /status/schema/awaiting-upgrade

exec "$@"
