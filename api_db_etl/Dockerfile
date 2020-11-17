FROM python:3.7-alpine

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make postgresql-dev

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY entrypoint.sh /
COPY app /app

ENV PYTHONPATH ${PYTHONPATH}:/

# depends on a volume mounted at /status/schema (managed by docker-compose)
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "app.run"]