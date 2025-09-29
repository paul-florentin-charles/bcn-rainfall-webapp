from bcn_rainfall_webapp.db import DBClient

db_client = DBClient.from_config()

# TODO: these variables should not be fixed but set up dynamically from UI
NORMAL_YEAR = 1981
BEGIN_YEAR = 1995
END_YEAR = 2024

__version__ = "1.1.3"

__all__ = [
    "__version__",
    "db_client",
    "NORMAL_YEAR",
    "BEGIN_YEAR",
    "END_YEAR",
]
