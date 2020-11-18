SHELL=/bin/bash
ETL_CONTAINER_NAME=api_db_etl
PGADMIN_CONTAINER_NAME=api_db_pgadmin
MIGRATION_MONITOR_CONTAINER_NAME=api_db_migration_monitor

build:
	docker-compose build

start_db:
	docker-compose up -d
	docker-compose logs -f $(MIGRATION_MONITOR_CONTAINER_NAME)
	docker cp api_db_pgadmin/pgadmin4-servers.json $(PGADMIN_CONTAINER_NAME):/tmp/pgadmin4-servers.json
	docker exec -it $(PGADMIN_CONTAINER_NAME) /bin/sh -c "python setup.py --load-servers /tmp/pgadmin4-servers.json --user admin"
	@echo "### Don't worry about duplicate errors if you have already created this couch database"
	make populate_couch

populate_couch:
	./create_couchdb_database.sh
	./load_couchdb_test_data.sh

stop_db:
	docker-compose down

fauxton:
	open http://localhost:5984/_utils/
	@echo "u/ admin"
	@echo "p/ password"

psql:
	docker exec -it online_db /bin/bash -c "PGPASSWORD=${POSTGRES_PASS} psql -U postgres -h localhost mermaid"

generate-migration:
	docker-compose exec $(ETL_CONTAINER_NAME) alembic -c /app/migrations/alembic.ini revision --autogenerate

new-migration:
	docker-compose exec $(ETL_CONTAINER_NAME) alembic -c /app/migrations/alembic.ini revision

apply-migration:
	docker-compose exec $(ETL_CONTAINER_NAME) alembic -c /app/migrations/alembic.ini upgrade head
