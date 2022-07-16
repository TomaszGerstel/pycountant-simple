DUMMY: test format path

# Run the tests with `make test` command
test:
		pytest tests

lint:
		flake8 pycountant

checks: lint test

format:
		black .
