#!/usr/bin/env python

"""
Script to run Flask server.
"""

import sys

import click
from a2wsgi import ASGIMiddleware
from redis.exceptions import ConnectionError as RedisConnectionError
from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from bcn_rainfall_webapp import Config, db_client
from bcn_rainfall_webapp.api.app import fastapi_app
from bcn_rainfall_webapp.app import flask_app


@click.command()
@click.option(
    "--use-redis-db",
    "-db",
    is_flag=True,
    help="Whether to use a running Redis DB to store API data or not.",
)
def run(use_redis_db):
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

    # 2. Mount both Flask and FastAPI applications together
    app = DispatcherMiddleware(
        flask_app,
        # Convert FastAPI app from ASGI to WSGI
        {"/rest": ASGIMiddleware(fastapi_app)},  # type: ignore
    )

    # 3. Run final mounted application
    config = Config()
    run_simple(
        config.get_webapp_server_settings.host,
        config.get_webapp_server_settings.port,
        app,
        use_reloader=config.get_webapp_server_settings.debug or False,
        threaded=True,
    )


if __name__ == "__main__":
    run()
