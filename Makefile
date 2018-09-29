.PHONY: default

default: test

install:
	pipenv install 

test:
#	PYTHONPATH=./src pipenv run pytest
	PYTHONPATH=./src pytest
