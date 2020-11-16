SHELL=/bin/bash

start_db:
	docker-compose up -d

	@echo "Sleeping for 10 seconds to let databases spin up! (ー。ー) zzz"
	@sleep 10

stop_db:
	docker-compose down

kill_db:
	docker-compose down -v

fauxton:
	open http://localhost:5984/_utils/
	@echo "u/ admin"
	@echo "p/ password"

psql:
	docker exec -it online_db /bin/bash -c "PGPASSWORD=${POSTGRES_PASS} psql -U postgres -h localhost mermaid"
