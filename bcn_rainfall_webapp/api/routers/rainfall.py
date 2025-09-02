from flask_openapi3 import APIBlueprint

rainfall_blueprint = APIBlueprint("rainfall", __name__, url_prefix="/rainfall")
