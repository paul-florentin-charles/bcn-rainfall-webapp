from flask_openapi3 import APIBlueprint


def populate_blueprint(api_blueprint: APIBlueprint):
    from bcn_rainfall_webapp.api.routers.csv import csv_blueprint
    from bcn_rainfall_webapp.api.routers.graph import graph_blueprint
    from bcn_rainfall_webapp.api.routers.rainfall import rainfall_blueprint
    from bcn_rainfall_webapp.api.routers.year import year_blueprint

    api_blueprint.register_api(csv_blueprint)
    api_blueprint.register_api(graph_blueprint)
    api_blueprint.register_api(rainfall_blueprint)
    api_blueprint.register_api(year_blueprint)


__all__ = ["populate_blueprint"]
