from bcn_rainfall_api_client import APIClient
from redis import Redis

from bcn_rainfall_webapp.config import Config

api_client = APIClient(base_url=Config().get_fastapi_base_url)
redis_client = Redis(**Config().get_redis_server_settings.model_dump())

NORMAL_YEAR = 1981
BEGIN_YEAR = 1995
END_YEAR = 2024

__version__ = "1.0.4"

__all__ = ["api_client", "redis_client", "NORMAL_YEAR", "BEGIN_YEAR", "END_YEAR"]
