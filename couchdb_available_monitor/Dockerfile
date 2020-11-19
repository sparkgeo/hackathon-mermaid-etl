FROM alpine:3.9

COPY monitor.sh /

# depends on a volume mounted at /status/couchdb (managed by docker-compose)
CMD /bin/sh /monitor.sh
