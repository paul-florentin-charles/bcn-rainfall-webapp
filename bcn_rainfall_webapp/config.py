"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from functools import cached_property
from typing import Optional

from bcn_rainfall_webapp.utils import BaseConfig, WebappServerSettings


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
    def get_webapp_server_settings(self) -> WebappServerSettings:
        """
        Return Flask server settings.

        Example:
        {
            "host": "127.0.0.1",
            "port": 5000,
            "debug": True,
        }
        """

        return WebappServerSettings(**self.yaml_config["webapp"])

    @cached_property
    def get_fastapi_base_url(self) -> str:
        """
        Return FastAPI base URL.

        Example: "https://bcn-rainfall-api.onrender.com/rest".
        """
        return self.yaml_config["api_base_url"]
