SHELL := /bin/bash
PWD := $(shell pwd)

default: build

all:

docker-images:
	docker build -f ./server/Dockerfile -t "eia-server:latest" ./server
	docker build -f ./backoffice/eia-ui/Dockerfile -t "eia-ui:latest" ./backoffice/eia-ui

run: docker-images
	docker-compose -f docker-compose.yaml up --remove-orphans --build

down:
	docker-compose -f docker-compose.yaml stop -t 1
	docker-compose -f docker-compose.yaml down -v
	docker network prune -f
	docker container prune -f
	docker image prune -f

logs-server:
	docker-compose -f docker-compose.yaml logs -f eia-server

logs-ui:
	docker-compose -f docker-compose.yaml logs -f eia-ui
