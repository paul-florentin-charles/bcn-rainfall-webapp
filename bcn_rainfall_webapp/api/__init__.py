from bcn_rainfall_core import Rainfall
from flask import jsonify
from flask_openapi3 import APIBlueprint

from bcn_rainfall_webapp import Config
from bcn_rainfall_webapp.api.routers import populate_blueprint

all_rainfall = Rainfall.from_config()

MIN_YEAR_AVAILABLE: int = all_rainfall.starting_year
MAX_YEAR_AVAILABLE: int = all_rainfall.get_last_year()
MAX_NORMAL_YEAR_AVAILABLE = MAX_YEAR_AVAILABLE - 29

api_blueprint = APIBlueprint(
    "api", __name__, url_prefix=Config().get_api_settings.root_path
)
populate_blueprint(api_blueprint)


@api_blueprint.errorhandler(400)
def bad_request(e):
    return jsonify({"detail": str(e.description)}), 400


__all__ = [
    "all_rainfall",
    "api_blueprint",
    "MIN_YEAR_AVAILABLE",
    "MAX_YEAR_AVAILABLE",
    "MAX_NORMAL_YEAR_AVAILABLE",
]
