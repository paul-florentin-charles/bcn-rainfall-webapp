from flask_openapi3 import APIBlueprint, Tag

graph_blueprint = APIBlueprint(
    "graph", __name__, url_prefix="/graph", abp_tags=[Tag(name="Graph")]
)
