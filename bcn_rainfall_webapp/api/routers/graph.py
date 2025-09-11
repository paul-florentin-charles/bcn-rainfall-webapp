from bcn_rainfall_core.utils import Label, TimeMode
from flask import abort
from flask_openapi3 import APIBlueprint, Tag

from bcn_rainfall_webapp.api import MAX_YEAR_AVAILABLE, all_rainfall
from bcn_rainfall_webapp.api.schemas import (
    APIQueryParametersForRainfallByYear,
    APIQueryParametersMinimal,
    APIQueryParametersMinimalWithNormal,
    APIQueryParametersMinimalWithWeighByAverage,
    APIQueryParametersWithPercentagesOfNormal,
)
from bcn_rainfall_webapp.api.utils import (
    raise_time_mode_error_or_do_nothing,
    raise_year_related_error_or_do_nothing,
)

graph_blueprint = APIBlueprint(
    "graph", __name__, url_prefix="/graph", abp_tags=[Tag(name="Graph")]
)


@graph_blueprint.get(
    "/rainfall_by_year",
    summary="Retrieve rainfall by year as a JSON.",
    description="Could either be for rainfall upon a whole year, a specific month or a given season.<br>"
    f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={
        "200": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                    }
                }
            },
            "description": "Plotly graph as JSON",
        }
    },
)
def get_rainfall_by_year_as_plotly_json(query: APIQueryParametersForRainfallByYear):
    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)
    raise_time_mode_error_or_do_nothing(query.time_mode, query.month, query.season)

    figure = all_rainfall.get_bar_figure_of_rainfall_according_to_year(
        query.time_mode,
        begin_year=query.begin_year,
        end_year=query.end_year,
        month=query.month,
        season=query.season,
        plot_average=query.plot_average,
        plot_linear_regression=query.plot_linear_regression,
        kmeans_cluster_count=query.kmeans_cluster_count,
    )
    if figure is None:
        abort(
            400,
            description=f"Data has not been successfully plotted, "
            f"check if your data has both '{Label.RAINFALL.value}' and '{Label.YEAR.value}' columns.",
        )

    return figure.to_json()


@graph_blueprint.get(
    "/rainfall_averages",
    summary="Retrieve rainfall monthly or seasonal averages of data as a JSON.",
    description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
    f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={
        "200": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                    }
                }
            },
            "description": "Plotly graph as JSON",
        }
    },
)
def get_rainfall_averages_as_plotly_json(query: APIQueryParametersMinimal):
    if query.time_mode == TimeMode.YEARLY:
        abort(
            400,
            description=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)

    return all_rainfall.get_bar_figure_of_rainfall_averages(
        time_mode=query.time_mode, begin_year=query.begin_year, end_year=query.end_year
    ).to_json()


@graph_blueprint.get(
    "/rainfall_linreg_slopes",
    summary="Retrieve rainfall monthly or seasonal linear regression slopes of data as a JSON.",
    description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
    f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={
        "200": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                    }
                }
            },
            "description": "Plotly graph as JSON",
        }
    },
)
def get_rainfall_linreg_slopes_as_plotly_json(query: APIQueryParametersMinimal):
    if query.time_mode == TimeMode.YEARLY:
        abort(
            400,
            description=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)

    return all_rainfall.get_bar_figure_of_rainfall_linreg_slopes(
        time_mode=query.time_mode, begin_year=query.begin_year, end_year=query.end_year
    ).to_json()


@graph_blueprint.get(
    "/relative_distances_to_normal",
    summary="Retrieve monthly or seasonal relative distances to normal (%) of data as a JSON.",
    description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
    f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={
        "200": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                    }
                }
            },
            "description": "Plotly graph as JSON",
        }
    },
)
def get_relative_distances_to_rainfall_normal_as_plotly_json(
    query: APIQueryParametersMinimalWithNormal,
):
    if query.time_mode == TimeMode.YEARLY:
        abort(
            400,
            description=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)

    return all_rainfall.get_bar_figure_of_relative_distance_to_normal(
        time_mode=query.time_mode,
        normal_year=query.normal_year,
        begin_year=query.begin_year,
        end_year=query.end_year,
    ).to_json()


@graph_blueprint.get(
    "/standard_deviations",
    summary="Retrieve monthly or seasonal standard deviations (mm) of data as a JSON.",
    description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
    f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={
        "200": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                    }
                }
            },
            "description": "Plotly graph as JSON",
        }
    },
)
def get_rainfall_standard_deviations_as_plotly_json(
    query: APIQueryParametersMinimalWithWeighByAverage,
):
    if query.time_mode == TimeMode.YEARLY:
        abort(
            400,
            description=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)

    return all_rainfall.get_bar_figure_of_standard_deviations(
        time_mode=query.time_mode,
        begin_year=query.begin_year,
        end_year=query.end_year,
        weigh_by_average=query.weigh_by_average,
    ).to_json()


@graph_blueprint.get(
    "/percentage_of_years_above_and_below_normal",
    summary="Retrieve pie chart of years above compared to years below normal (%) of data as a JSON.",
    description=f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={
        "200": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                    }
                }
            },
            "description": "Plotly graph as JSON",
        }
    },
)
def get_percentage_of_years_above_and_below_normal_as_plotly_json(
    query: APIQueryParametersWithPercentagesOfNormal,
):
    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)
    raise_time_mode_error_or_do_nothing(query.time_mode, query.month, query.season)

    return all_rainfall.get_pie_figure_of_years_above_and_below_normal(
        time_mode=query.time_mode,
        normal_year=query.normal_year,
        begin_year=query.begin_year,
        end_year=query.end_year,
        month=query.month,
        season=query.season,
        percentages_of_normal=tuple(
            float(percent)
            for percent in query.percentages_of_normal.split(",")
            if percent
        ),
    ).to_json()
