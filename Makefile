.PHONY: default

default: test

install:
	pipenv install --dev --skip-lock

test:
#	PYTHONPATH=./src pipenv run pytest
	PYTHONPATH=./src pytest
