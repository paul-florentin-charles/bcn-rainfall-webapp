#!/usr/bin/env python

"""
Script to run Flask server.
"""

from bcn_rainfall_webapp.app import flask_app
from bcn_rainfall_webapp.config import Config


def run():
    flask_app.run(**Config().get_webapp_server_settings.model_dump())


if __name__ == "__main__":
    run()
