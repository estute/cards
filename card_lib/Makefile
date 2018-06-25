SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

help:
	@echo ''
	@echo 'make help             show this information'
	@echo 'make requirements     install requirements for testing'
	@echo 'make test             run unit tests'

requirements:
	pip install -r requirements.txt

test:
	pytest .
