# pycountant-simple

## Contributing guide

### Virtual environment
Use virtual environment (on Linux: `python -m venv .venv` then `. .venv/bin/activate` and update the environment with `pip install -r requirements.txt`).

If you need any Python package available from pip, install it `pip install <package-name>` and remember to update `requirements.txt` with
`pip freeze > requirements.txt`

### Before each commit
Before each commit, run tests and linting with `make checks`


### Docker with Docker Compose
Use `docker-compose up --build` to build the app on your machine.
Since your main directory is mounted as a volume in `docker-compose.yml`, the server will automatically refresh after your source code modifications.
Fast feedback!


### Sample data
To use sample data run `create_db` and then run `add_sample_data` from `db` package.
You can also add before some sample data to `pycountant.sample_data`.
