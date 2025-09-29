"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from functools import cached_property
from typing import Optional

from bcn_rainfall_webapp.utils import (
    APISettings,
    BaseConfig,
    DevelopmentServerSettings,
    ProductionServerSettings,
    RedisServerSettings,
)


class Config(BaseConfig):
    """
    Provides function to retrieve fields from YAML configuration.
    It needs to be instantiated first to be loaded.
    Configuration is cached but can be reloaded if needed.
    """

    _instance: Optional["Config"] = None

    def __new__(cls, *, path="config.yml"):
        return super().__new__(cls, path=path)

    @cached_property
    def get_production_server_settings(self) -> ProductionServerSettings:
        """
        Return Waitress server settings.

        Example:
        {
            "host": "127.0.0.1",
            "port": 8080,
        }
        """

        return ProductionServerSettings(**self.yaml_config["server"]["prod"])

    @cached_property
    def get_development_server_settings(self) -> DevelopmentServerSettings:
        """
        Return Flask server settings.

        Example:
        {
            "host": "127.0.0.1",
            "port": 5000,
            "debug": True,
        }
        """

        return DevelopmentServerSettings(**self.yaml_config["server"]["dev"])

    @cached_property
    def get_redis_server_settings(self) -> RedisServerSettings:
        """
        Return Redis server settings.

        Example:
        {
            "host": "localhost",
            "port": 6379,
            "db": 0,
        }
        """

        return RedisServerSettings(**self.yaml_config["redis"])

    @cached_property
    def get_api_settings(self) -> APISettings:
        """
        Return API settings.

        Example:
        {
            "root_path": "/rest",
            "title": "Barcelona Rainfall API",
            "summary": "An API that provides rainfall-related data of the city of Barcelona.",
        }

        """

        return APISettings(**self.yaml_config["api"])
