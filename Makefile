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
clean-venv: ## clean venv
	poetry env remove --all
clean-data: ## clean data
	rm -rf ./code/data
	rm -rf ./data
clean-log: ## clean log
	rm -rf ./code/*.log
	rm -rf ./*.log
clean-env: ## clean env
	rm -rf ./code/__pycache__

rebuid: clean-env install ## rebuild poetry

uploda-clean: clean-data clean-log clean-env ## clean file before git push

help: ## print help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

