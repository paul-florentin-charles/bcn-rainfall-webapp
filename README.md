# bcn-rainfall-webapp

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Webapp run with Flask to display in a user-friendly way rainfall data from the city of Barcelona that is retrieved from
the Barcelona Rainfall API using its client.

### Requirements

- Python 3.12
- Pip

### Get started

#### Build

```commandline
git clone https://github.com/paul-florentin-charles/bcn-rainfall-webapp.git
cd bcn-rainfall-webapp
pip install uv
uv sync
```

#### Run

With default settings retrieved from `config.yml`

```commandline
uv run run.py
```

With your own server settings

```commandline
uv run flask --app bcn_rainfall_webapp.app:flask_app --host localhost --port 5050 --debug run
```

:warning: Make sure that `bcn_rainfall_webapp.app` is the correct path to app object and that `flask_app` is the correct app instance name.

### Code quality

```commandline
uv tool run mypy --check-untyped-defs .
uv tool run ruff check
uv tool run ruff format
```