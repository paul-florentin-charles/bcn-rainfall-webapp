#!/usr/bin/env python

"""
Script to run Flask server.
"""

import sys

import click
from redis.exceptions import ConnectionError as RedisConnectionError
from requests.exceptions import ConnectionError as RequestsConnectionError

from bcn_rainfall_webapp import api_client, db_client
from bcn_rainfall_webapp.app import openapi_app
from bcn_rainfall_webapp.config import Config


@click.command()
@click.option(
    "--use-redis-db",
    "-db",
    is_flag=True,
    help="Whether to use a running Redis DB to store API data or not.",
)
def run(use_redis_db):
    # 1. Make sure API is running so that we can retrieve data.
    try:
        api_client.head_api("/", timeout=3)
    except RequestsConnectionError:
        sys.exit(
            f"Cannot connect to API at '{api_client.base_url}', make sure it is running."
        )

    # 2. Make sure DB is running if `use_redis_db` is True, otherwise disable DB client.
    if use_redis_db:
        try:
            db_client.client.ping()
        except RedisConnectionError:
            sys.exit(
                f"Cannot connect to Redis Server DB#{db_client.db} at '{db_client.host}:{db_client.port}', make sure it is running."
            )
    else:
        db_client.disable()

    # 3. Run Webapp
    openapi_app.run(**Config().get_webapp_server_settings.model_dump())


if __name__ == "__main__":
    run()
