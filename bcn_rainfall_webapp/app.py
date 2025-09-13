"""
Webapp run with Flask that communicates with an API (FastAPI/Uvicorn) to display rainfall-related data.
Work-in-progress!
"""

from flask_openapi3 import Info, OpenAPI

from bcn_rainfall_webapp import __version__
from bcn_rainfall_webapp.api import api_blueprint
from bcn_rainfall_webapp.config import Config
from bcn_rainfall_webapp.views import webapp_blueprint

openapi_app = OpenAPI(
    __name__,
    info=Info(
        title=Config().get_api_settings.title,
        summary=Config().get_api_settings.summary,
        version=__version__,
    ),
)

# Register Webapp routes
openapi_app.register_blueprint(webapp_blueprint)

# Register API routes
openapi_app.register_api(api_blueprint)
