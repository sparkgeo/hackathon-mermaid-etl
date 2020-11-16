Hackathon Mermaid ETL
---------------------


_Part of the MERMAID Replugged project_


## Prerequisites

- Docker (https://docs.docker.com/engine/install/)
- docker-compose (https://docs.docker.com/compose/install/)



## Environment Variables

```
COUCHDB_USER=admin
COUCHDB_PASSWORD=password
```

## Spin up local development


Start CouchDB and PostgreSQL databases

`make start_db`

Stop CouchDB and PostgreSQL databases

`make stop_db`

Load CouchDB admin page in browser

```
make fauxton

user/ admin
password/ password

```

Access psql

```
make psql

```




