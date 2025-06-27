#!/usr/bin/env python

"""
Script to run Flask server.
"""

import sys

from redis.exceptions import ConnectionError as RedisConnectionError
from requests.exceptions import ConnectionError as RequestsConnectionError

from bcn_rainfall_webapp import api_client, redis_client
from bcn_rainfall_webapp.app import flask_app
from bcn_rainfall_webapp.config import Config


def run():
    # 1. Make sure API is running
    try:
        api_client.head_api("/", timeout=3)
    except RequestsConnectionError:
        sys.exit(
            f"Cannot connect to API at '{api_client.base_url}', make sure it is running."
        )

    # 2. Make sure DB is running
    try:
        redis_client.ping()
    except RedisConnectionError:
        sys.exit(
            f"Cannot connect to Redis Server at '{redis_client.connection_pool}', make sure it is running."
        )

    # 3. Run Webapp
    flask_app.run(**Config().get_webapp_server_settings.model_dump())


if __name__ == "__main__":
    run()
