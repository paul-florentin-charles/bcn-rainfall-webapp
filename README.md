# bcn-rainfall-webapp

[![GitHub version](https://badge.fury.io/gh/paul-florentin-charles%2Fbcn-rainfall-webapp.svg)](https://badge.fury.io/gh/paul-florentin-charles%2Fbcn-rainfall-webapp)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![coverage badge](coverage.svg)](https://github.com/nedbat/coveragepy)  
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)  
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)  
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Webapp run with Flask to display in a user-friendly way rainfall data from the city of Barcelona.

It exposes an **API** whose docs can be found at `/openapi`.

## Requirements

- Python 3.12
- Pip
- Redis server (optional for performance)

## Get started

### With Docker

```commandline
git clone https://github.com/paul-florentin-charles/bcn-rainfall-webapp.git  
cd bcn-rainfall-webapp
docker compose up --build
```

### Without

#### Build

```commandline  
git clone https://github.com/paul-florentin-charles/bcn-rainfall-webapp.git  
cd bcn-rainfall-webapp  
pip install uv  
uv sync  
```  

#### Install and run Redis server (optional)

```commandline  
sudo apt install redis  
sudo systemctl status redis-server  
```  

#### Run Flask Webapp server

 ```commandline  
 uv run run.py [--use-redis-db] [--for-production]  
 ``` 

## Tests & Coverage

```commandline  
uv run coverage run -m pytest  
uv run coverage report  
```  

## Code quality

### Python

```commandline  
uv tool run mypy --check-untyped-defs .  
uv tool run ruff check  
uv tool run ruff format  
uv tool run pyupgrade --py312-plus **/*.py  
```  

### JavaScript

```commandline  
cd bcn_rainfall_webapp/static  
npm install  
npx eslint js  
```
