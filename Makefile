build:
	docker-compose build server

run: build
	docker-compose up server

db:
	docker-compose up postgress_bd

lint:
	docker-compose up lint

format:
	docker-compose up format