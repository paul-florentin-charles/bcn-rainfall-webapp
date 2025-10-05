import hashlib
import json
from datetime import datetime

from bcn_rainfall_webapp.utils import RedisServerSettings


def get_hash_key(**kwargs) -> str:
    """
    Return a hash string using SHA256 algorithm applied to the JSON dict built with the sorted kwargs.

    :param kwargs: any arguments that can be hashed.
    :return: a hash string.
    """
    return hashlib.sha256(json.dumps(kwargs, sort_keys=True).encode()).hexdigest()


def get_seconds_until_end_of_the_day() -> int:
    """
    Compute and return the approximate number of seconds until the end of the current day.

    :return: a number of seconds as an int.
    """
    now = datetime.now()  # Current time
    end_of_day = datetime.combine(now.date(), datetime.max.time())  # End of the day

    return int((end_of_day - now).total_seconds())


def get_redis_server_settings_from_url(url: str) -> RedisServerSettings:
    host, port, db = (*url.split("@")[1].split(":"), "0")
    if "/" in port:
        port, db = port.split("/")
    elif "?db=" in port:
        port, db = port.split("?db=")

    return RedisServerSettings(
        host=host,
        port=int(port),
        db=int(db),
    )
