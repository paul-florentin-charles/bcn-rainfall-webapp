#!/usr/bin/env python

"""
Script to run Flask server.
"""
import sys

from requests.exceptions import ConnectionError

from bcn_rainfall_webapp import api_client
from bcn_rainfall_webapp.app import flask_app
from bcn_rainfall_webapp.config import Config


def run():
    # 1. Make sure API is running
    try:
        api_client.head_api('/', timeout=3)
    except ConnectionError:
        sys.exit(f"Cannot connect to API at '{api_client.base_url}', make sure it is running.")

    # 2. Run Webapp
    flask_app.run(**Config().get_webapp_server_settings.model_dump())


if __name__ == "__main__":
    run()
