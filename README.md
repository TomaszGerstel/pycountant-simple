# pycountant-simple

## Contributing guide

### Virtual environment
Use virtual environment (on Linux: `python -m venv .venv` then `. ./venv/bin/activate` and update the environment with `pip install -r requirements.txt`).

If you need any Python package available from pip, install it `pip install <package-name>` and remember to update `requirements.txt` with
`pip freeze > requirements.txt`

### Before each commit
Before each commit, run tests and linting with `make checks`