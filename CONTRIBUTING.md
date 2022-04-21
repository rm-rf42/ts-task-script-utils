# Developer Information for `ts-task-script-utils`

## Environment setup

### Python Setup

Use `pyenv` to switch between multiple independent versions of Python. This avoids installing dependencies into the system Python or otherwise changing its configuration. See [the pyenv documentation](https://github.com/pyenv/pyenv#installation) for installation instructions.

### Virtual Environment Setup

`ts-task-script-utils` uses `poetry` to manage dependencies, set up the virtual environment setup, and build distributions. To use `poetry`, install it into the desired Python and then create the virtual environment using `poetry install`. In the example code below, Python 3.7.12 and `poetry` 1.1.12 are used, but installation should work with Python >=3.7,<4 and `poetry` >=1.1.0.

```shell
# cd into the repository root directory
cd ts-task-script-utils
pyenv local 3.7.12
pip install poetry
# For easier cleanup and inspection of the virtual environment, it's recommended
# to install the virtual environment in the repository root. To do this, set the
# environment variable `POETRY_VIRTUALENVS_IN_PROJECT` to `true`.
export POETRY_VIRTUALENVS_IN_PROJECT=true
poetry install
```

The above will create a Python 3.7.12 virtual environment in a `.venv` directory in the repository root.

## Code Formatting

`ts-task-script-utils` formats Python code using `black`. To format the code, run

```shell
poetry run black .
```

`black` is configured in `pyproject.toml`, in the section `[tool.black]`. For more info see the `black` documentation [here](https://black.readthedocs.io/en/stable/).

## Running tests

`ts-task-script-utils` uses `pytest` as its testing framework. As such, tests can be executed with the `pytest` shell command (see the [pytest docs here](https://docs.pytest.org/en/latest/how-to/usage.html)). Note that `pytest-cov`, a `pytest` plugin dependency of `ts-task-script-utils`, prevents one from running individual tests; any attempt to run a single test runs the entire test module. To turn off `pytest-cov` and thus enable running individual tests, pass the `--no-cov` flag to the `pytest` command. For example, to run the `TestMyExampleClass.test_my_examle_method` test located at `tests/test_my_module.py`, do

```shell
pytest --no-cov tests/test_my_module.py::TestMyExampleClass::test_my_examle_method
```

## Publishing the package

### Set your package's version

`poetry` derives the package version from the `pyproject.toml` file. To set the version to, for example, `v1.2.3`, do

```shell
poetry version 1.2.3
```

This will update the appropriate section of `pyproject.toml`. You should create a PR and merge into `main`, and, if applicable, into `development` as well. This may also be done as part of another PR.

Note: do not prepend the version with a `v`. This not supported by `poetry` nor PyPi. For further info on the `poetry version` command see the [poetry documentation here](https://python-poetry.org/docs/cli/#version).

### Build and publish the Python package

Building and publishing the Python package to the appropriate Python package server is done in continuous integration (CI). See `.github/workflows/publish.yml`.
