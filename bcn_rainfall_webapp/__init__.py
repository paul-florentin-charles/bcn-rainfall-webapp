from bcn_rainfall_webapp.db import DBClient

db_client = DBClient.from_config()

NORMAL_YEAR = 1981
BEGIN_YEAR = 1995
END_YEAR = 2024

__version__ = "1.1.2"

__all__ = [
    "__version__",
    "db_client",
    "NORMAL_YEAR",
    "BEGIN_YEAR",
    "END_YEAR",
]
