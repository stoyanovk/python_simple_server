build:
	docker-compose build server

run:
	docker-compose up server

fill-db:
	docker-compose run fill-db

db:
	docker-compose up postgress_bd

redis:
	docker-compose up redis

lint: build
	docker-compose run lint

format: build
	docker-compose run format

check-format: build
	docker-compose run check-format

types: build
	docker-compose run types

tests: build
	docker-compose run tests