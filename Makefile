DUMMY: test format

# Run the tests with `make test` command
test:
		pytest countant_test.py && pytest tests

format:
		black .
