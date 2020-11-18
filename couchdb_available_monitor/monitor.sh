#!/bin/sh

set -e

sleep 1
while [ -f "/status/couchdb/awaiting-database" ]
do
  echo "couchdb not yet available..."
  sleep 1
done
echo "couchdb available"
