SHELL := /bin/bash
PWD := $(shell pwd)

default: build

all:

docker-images:
	docker build -f ./server/Dockerfile -t "open-lisa-server:latest" ./server

run: docker-images
	docker-compose -f docker-compose.yaml up --remove-orphans --build

down:
	docker-compose -f docker-compose.yaml stop -t 1
	docker-compose -f docker-compose.yaml down -v
	docker network prune -f
	docker container prune -f
	docker image prune -f

logs-server:
	docker-compose -f docker-compose.yaml logs -f open-lisa-server

