DUMMY: test format path update

# Run the tests with `make test` command
test:
		pytest tests

lint:
		flake8 pycountant

checks: lint test

format:
		black .

update:
		./update.sh

venv:
		python -m venv .venv

install:
		pip install -r requirements.txt

