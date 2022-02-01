SHELL := /bin/bash
PWD := $(shell pwd)

default: build

all:

docker-images:
	docker build -f ./server/Dockerfile -t "eia-server:latest" ./server
	docker build -f ./backoffice/eia-ui/Dockerfile -t "eia-ui:latest" ./backoffice/eia-ui
.PHONY: docker-images

run: docker-images
	docker-compose -f docker-compose.yaml up --remove-orphans --build
.PHONY: run

down:
	docker-compose -f docker-compose.yaml stop -t 1
	docker-compose -f docker-compose.yaml down -v
	docker network prune -f
	docker container prune -f
	docker image prune -f
.PHONY: down

logs-server:
	docker-compose -f docker-compose.yaml logs -f eia-server
.PHONY: logs-server

logs-ui:
	docker-compose -f docker-compose.yaml logs -f eia-ui
.PHONY: logs-ui
