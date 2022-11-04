precommit-install:
	pip3 install pre-commit
	pre-commit install

lint:
	pre-commit run --all-files

up:
	bash start.sh
