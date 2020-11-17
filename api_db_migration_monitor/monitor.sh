#!/bin/sh

set -e

sleep 1
while [ -f "/status/schema/awaiting-upgrade" ]
do
  echo "Schema undergoing migration..."
  sleep 1
done
echo "Schema migration complete"
