Hackathon Mermaid ETL
---------------------


_Part of the MERMAID Replugged project_


## Prerequisites

- Docker (https://docs.docker.com/engine/install/)
- docker-compose (https://docs.docker.com/compose/install/)



## Environment Variables

Copy the following into a `.env` file (see `.env_sample`)
```
COUCHDB_USER=admin
COUCHDB_PASSWORD=password
POSTGRES_DB=mermaid
POSTGRES_PASS=postgres
POSTGRES_USER=postgres
POSTGRES_DBNAME=mermaid
POSTGRES_MULTIPLE_EXTENSIONS=postgis,hstore,postgis_topology,postgis_raster,pgrouting
PGADMIN_DEFAULT_EMAIL=admin
PGADMIN_DEFAULT_PASSWORD=admin
PGADMIN_LISTEN_ADDRESS=api_db_pgadmin
PGADMIN_LISTEN_PORT=5050
```

## Spin up local development


Start CouchDB and PostgreSQL databases

`make build && make start_db`

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
or 
```
http://localhost:5050

user/ admin
password/ admin
```



