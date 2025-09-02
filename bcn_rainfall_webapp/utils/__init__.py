from bcn_rainfall_webapp.utils.base_config import BaseConfig
from bcn_rainfall_webapp.utils.graph import DEFAULT_LAYOUT
from bcn_rainfall_webapp.utils.schemas import (
    APISettings,
    RedisServerSettings,
    WebappServerSettings,
)

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
SEASONS = ["spring", "summer", "fall", "winter"]


__all__ = [
    "BaseConfig",
    "RedisServerSettings",
    "WebappServerSettings",
    "APISettings",
    "MONTHS",
    "SEASONS",
    "DEFAULT_LAYOUT",
]
