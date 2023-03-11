build:
	docker-compose build server

run: build
	docker-compose up server

db:
	docker-compose up postgress_bd

redis:
	docker-compose up redis

lint: build
	docker-compose run lint

format: build
	docker-compose run format