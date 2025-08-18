"""
Module to provide a function that returns a dict linking FastAPI routes endpoints to their specifications.
"""

from typing import Any, Callable

from bcn_rainfall_core import Rainfall
from bcn_rainfall_core.utils import TimeMode
from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse, StreamingResponse

from bcn_rainfall_webapp.api.utils import RainfallModel

all_rainfall = Rainfall.from_config(from_file=True)


MIN_YEAR_AVAILABLE = all_rainfall.starting_year
MAX_YEAR_AVAILABLE = all_rainfall.get_last_year()
MAX_NORMAL_YEAR_AVAILABLE = MAX_YEAR_AVAILABLE - 29

__all__ = [
    "all_rainfall",
    "get_endpoint_to_api_route_specs_by_router_name",
    "MIN_YEAR_AVAILABLE",
    "MAX_YEAR_AVAILABLE",
    "MAX_NORMAL_YEAR_AVAILABLE",
    "ROUTER_BY_NAME",
]

ROUTER_BY_NAME: dict[str, APIRouter] = {
    "rainfall": APIRouter(prefix="/rainfall", tags=["Rainfall"]),
    "year": APIRouter(prefix="/year", tags=["Year"]),
    "graph": APIRouter(prefix="/graph", tags=["Graph"]),
    "csv": APIRouter(prefix="/csv", tags=["CSV"]),
}


class APIRouteSpecs(BaseModel):
    path: str
    summary: str
    description: str | None = Field(default=None)
    response_model: Any = Field(default=None)
    tags: list[str] = Field(default_factory=list)
    response_class: Any = Field(default=JSONResponse)


def get_endpoint_to_api_route_specs_by_router_name() -> dict[
    str, dict[Callable[..., Any], APIRouteSpecs]
]:
    from bcn_rainfall_webapp.api.routes.csv import get_rainfall_by_year_as_csv
    from bcn_rainfall_webapp.api.routes.graph import (
        get_percentage_of_years_above_and_below_normal_as_plotly_json,
        get_rainfall_averages_as_plotly_json,
        get_rainfall_by_year_as_plotly_json,
        get_rainfall_linreg_slopes_as_plotly_json,
        get_relative_distances_to_normal_as_plotly_json,
        get_standard_deviations_as_plotly_json,
    )
    from bcn_rainfall_webapp.api.routes.rainfall import (
        get_rainfall_average,
        get_rainfall_normal,
        get_rainfall_relative_distance_to_normal,
        get_rainfall_standard_deviation,
    )
    from bcn_rainfall_webapp.api.routes.year import (
        get_years_above_normal,
        get_years_below_normal,
    )

    endpoint_to_rainfall_api_route_specs: dict[Callable[..., Any], APIRouteSpecs] = {
        get_rainfall_average: APIRouteSpecs(
            path="/average",
            summary="Retrieve rainfall average for Barcelona between two years.",
            description=f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_rainfall_normal: APIRouteSpecs(
            path="/normal",
            summary="Retrieve 30 years rainfall average for Barcelona after a given year.",
            description="Commonly called rainfall normal.",
        ),
        get_rainfall_relative_distance_to_normal: APIRouteSpecs(
            path="/relative_distance_to_normal",
            summary="Retrieve the rainfall relative distance to normal for Barcelona between two years.",
            description="The metric is a percentage that can be negative. <br>"
            "Its formula is `(average - normal) / normal * 100`. <br> "
            "1. `average` is average rainfall computed between `begin_year` and `end_year`<br>"
            "2. `normal` is normal rainfall computed from `normal_year`<br>"
            "If 100%, average is twice the normal. <br>"
            "If -50%, average is half the normal. <br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_rainfall_standard_deviation: APIRouteSpecs(
            path="/standard_deviation",
            summary="Compute the standard deviation of rainfall for Barcelona between two years.",
            description=f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
    }

    for endpoint in endpoint_to_rainfall_api_route_specs.keys():
        endpoint_to_rainfall_api_route_specs[endpoint].response_model = RainfallModel

    endpoint_to_year_api_route_specs: dict[Callable[..., Any], APIRouteSpecs] = {
        get_years_below_normal: APIRouteSpecs(
            path="/below_normal",
            summary="Compute the number of years below normal for a specific year range.",
            description="Normal is computed as a 30 years average "
            f"starting from the year set via normal_year. <br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_years_above_normal: APIRouteSpecs(
            path="/above_normal",
            summary="Compute the number of years above normal for a specific year range.",
            description="Normal is computed as a 30 years average "
            f"starting from the year set via normal_year. <br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
    }

    for endpoint in endpoint_to_year_api_route_specs.keys():
        endpoint_to_year_api_route_specs[endpoint].response_model = RainfallModel

    endpoint_to_graph_api_route_specs: dict[Callable[..., Any], APIRouteSpecs] = {
        get_rainfall_by_year_as_plotly_json: APIRouteSpecs(
            path="/rainfall_by_year",
            summary="Retrieve rainfall by year as a PNG or as a JSON.",
            description="Could either be for rainfall upon a whole year, a specific month or a given season.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_rainfall_averages_as_plotly_json: APIRouteSpecs(
            path="/rainfall_averages",
            summary="Retrieve rainfall monthly or seasonal averages of data as a PNG or as a JSON.",
            description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_rainfall_linreg_slopes_as_plotly_json: APIRouteSpecs(
            path="/rainfall_linreg_slopes",
            summary="Retrieve rainfall monthly or seasonal linear regression slopes of data as a PNG or as a JSON.",
            description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_relative_distances_to_normal_as_plotly_json: APIRouteSpecs(
            path="/relative_distances_to_normal",
            summary="Retrieve monthly or seasonal relative distances to normal (%) of data as a PNG or as a JSON.",
            description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_standard_deviations_as_plotly_json: APIRouteSpecs(
            path="/standard_deviations",
            summary="Retrieve monthly or seasonal standard deviations (mm) of data as a PNG or as a JSON.",
            description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_percentage_of_years_above_and_below_normal_as_plotly_json: APIRouteSpecs(
            path="/percentage_of_years_above_and_below_normal",
            summary="Retrieve pie chart of years above compared to years below normal (%) of data as a JSON.",
            description=f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
    }

    endpoint_to_csv_api_route_specs: dict[Callable[..., Any], APIRouteSpecs] = {
        get_rainfall_by_year_as_csv: APIRouteSpecs(
            path="/rainfall_by_year",
            summary="Retrieve CSV of rainfall by year data: ['Year', 'Rainfall'] columns.",
            description="Could either be for rainfall upon a whole year, a specific month or a given season.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
            response_class=StreamingResponse,
        ),
    }

    return {
        "rainfall": endpoint_to_rainfall_api_route_specs,
        "year": endpoint_to_year_api_route_specs,
        "graph": endpoint_to_graph_api_route_specs,
        "csv": endpoint_to_csv_api_route_specs,
    }
