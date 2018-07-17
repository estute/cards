SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help
.PHONY: clean requirements


help:
	@echo '     make help                     show this help information'
	@echo '     make clean.card_lib           remove any artifacts or compiled files from the card_lib project'
	@echo '     make requirements.card_lib    install python requirements for the card_lib project and tests'
	@echo '     make test.card_lib            run unit tests for the card_lib project'
	@echo '     make clean.game_server        kill the game_server container and remove it, as well as any artifacts or compiled files'
	@echo '     make build.game_server        build the game_server docker container'
	@echo '     make run.game_server          run the game_server container'


### General

clean: clean.game_server clean.card_lib

requirements: requirements.game_server requirements.card_lib

### Make targets for the card_lib

clean.card_lib:
	find card_lib -name '*pyc' |xargs -I {} rm {}

requirements.card_lib:
	pip install -r requirements/test.txt

test.card_lib:
	pytest card_lib

### Make targets for the game_server

clean.game_server:
	docker kill game_server || true
	docker rm game_server || true
	docker rmi game_server || true
	find game_server -name '*pyc' |xargs -I {} rm {}

requirements.game_server:
	pip install -r requirements/game_server.txt
	pip install -r requirements/test.txt

test.game_server:
	pytest game_server

build.game_server:
	docker build -t game_server -f docker/game_server.Dockerfile .

run.game_server:
	docker run --name game_server -p 8888:8888 --rm game_server
