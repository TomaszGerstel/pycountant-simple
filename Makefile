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
