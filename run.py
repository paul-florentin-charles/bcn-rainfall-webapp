#!/usr/bin/env python

"""
Script to run Flask server.
"""

import sys

import click
import waitress
from redis.exceptions import ConnectionError as RedisConnectionError

from bcn_rainfall_webapp import db_client
from bcn_rainfall_webapp.app import openapi_app
from bcn_rainfall_webapp.config import Config


@click.command()
@click.option(
    "--use-redis-db",
    "-db",
    is_flag=True,
    help="Whether to use a running Redis DB to store API data or not.",
)
@click.option(
    "--for-production",
    "-prod",
    is_flag=True,
    help="Whether to use Waitress to run the server or not.",
)
def run(use_redis_db, for_production):
    # 1. Make sure DB is running if `use_redis_db` is True, otherwise disable DB client.
    if use_redis_db:
        try:
            db_client.client.ping()
        except RedisConnectionError:
            sys.exit(
                f"Cannot connect to Redis Server DB#{db_client.db} at '{db_client.host}:{db_client.port}', make sure it is running."
            )
    else:
        db_client.disable()

    # 2. Run Webapp
    if for_production:
        prod_settings = Config().get_production_server_settings

        print(f"* Running on http://{prod_settings.host}:{prod_settings.port}")
        print("Press Ctrl+C to stop.")

        waitress.serve(openapi_app, **prod_settings.model_dump())
    else:
        openapi_app.run(**Config().get_development_server_settings.model_dump())


if __name__ == "__main__":
    run()
