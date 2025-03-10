from bcn_rainfall_api_client import APIClient

api_client = APIClient.from_config()

NORMAL_YEAR = 1981
BEGIN_YEAR = 1995
END_YEAR = 2024

__version__ = "1.0.2"

__all__ = ["api_client", "NORMAL_YEAR", "BEGIN_YEAR", "END_YEAR"]
