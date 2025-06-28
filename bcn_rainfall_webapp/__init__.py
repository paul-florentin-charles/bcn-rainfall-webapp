from bcn_rainfall_api_client import APIClient

from bcn_rainfall_webapp.config import Config
from bcn_rainfall_webapp.db import DBClient

api_client = APIClient(base_url=Config().get_fastapi_base_url)
db_client = DBClient.from_config()

NORMAL_YEAR = 1981
BEGIN_YEAR = 1995
END_YEAR = 2024

__version__ = "1.1.0"

__all__ = ["api_client", "db_client", "NORMAL_YEAR", "BEGIN_YEAR", "END_YEAR"]
