WORKING_DIR=$(shell pwd)
PROJECT_NAME=$(shell basename $(WORKING_DIR))
AUTHOR=$(shell whoami)
PATHON_VERSION=$(shell python -V | cut -d" " -f2)

init: ## init python virtual env by poetry
	poetry init --name=$(PROJECT_NAME) --description="" --author=$(AUTHOR) --python=$(PATHON_VERSION) -q
install: ## install python package from pyproject.toml
	poetry install

install-requestments: ## install package from requestments
	cat ./requestments.txt | xargx poetry add 

clean-toml: ## remove .toml
	rm -f *.toml
clean-env: ## clean env
	poetry env remove --all

rebuid: clean-env install ## rebuild poetry

clean: 

help: ## print help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

