from typing import Annotated

from bcn_rainfall_core.utils import Label, Month, Season, TimeMode
from fastapi import HTTPException, Query

import bcn_rainfall_webapp.api.utils.errors as http_err
from bcn_rainfall_webapp.api.routes import (
    MAX_NORMAL_YEAR_AVAILABLE,
    MAX_YEAR_AVAILABLE,
    MIN_YEAR_AVAILABLE,
    all_rainfall,
)


def get_rainfall_by_year_as_plotly_json(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
    plot_average: bool = False,
    plot_linear_regression: bool = False,
    kmeans_cluster_count: int | None = None,
):
    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    http_err.raise_year_related_error_or_do_nothing(begin_year, end_year)
    http_err.raise_time_mode_error_or_do_nothing(time_mode, month, season)

    figure = all_rainfall.get_bar_figure_of_rainfall_according_to_year(
        time_mode,
        begin_year=begin_year,
        end_year=end_year,
        month=month,
        season=season,
        plot_average=plot_average,
        plot_linear_regression=plot_linear_regression,
        kmeans_cluster_count=kmeans_cluster_count,
    )
    if figure is None:
        raise HTTPException(
            status_code=400,
            detail=f"Data has not been successfully plotted, "
            f"check if your data has both '{Label.RAINFALL.value}' and '{Label.YEAR.value}' columns.",
        )

    return figure.to_json()


def get_rainfall_averages_as_plotly_json(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
):
    if time_mode == TimeMode.YEARLY:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    http_err.raise_year_related_error_or_do_nothing(begin_year, end_year)

    return all_rainfall.get_bar_figure_of_rainfall_averages(
        time_mode=time_mode, begin_year=begin_year, end_year=end_year
    ).to_json()


def get_rainfall_linreg_slopes_as_plotly_json(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
):
    if time_mode == TimeMode.YEARLY:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    http_err.raise_year_related_error_or_do_nothing(begin_year, end_year)

    return all_rainfall.get_bar_figure_of_rainfall_linreg_slopes(
        time_mode=time_mode, begin_year=begin_year, end_year=end_year
    ).to_json()


def get_relative_distances_to_normal_as_plotly_json(
    time_mode: TimeMode,
    normal_year: Annotated[
        int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_NORMAL_YEAR_AVAILABLE)
    ],
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
):
    if time_mode == TimeMode.YEARLY:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    http_err.raise_year_related_error_or_do_nothing(begin_year, end_year)

    return all_rainfall.get_bar_figure_of_relative_distance_to_normal(
        time_mode=time_mode,
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
    ).to_json()


def get_standard_deviations_as_plotly_json(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    weigh_by_average: bool = False,
):
    if time_mode == TimeMode.YEARLY:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    http_err.raise_year_related_error_or_do_nothing(begin_year, end_year)

    return all_rainfall.get_bar_figure_of_standard_deviations(
        time_mode=time_mode,
        begin_year=begin_year,
        end_year=end_year,
        weigh_by_average=weigh_by_average,
    ).to_json()


def get_percentage_of_years_above_and_below_normal_as_plotly_json(
    time_mode: TimeMode,
    normal_year: Annotated[
        int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_NORMAL_YEAR_AVAILABLE)
    ],
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
    percentages_of_normal: str = "0,80,120,inf",
):
    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    http_err.raise_year_related_error_or_do_nothing(begin_year, end_year)
    http_err.raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return all_rainfall.get_pie_figure_of_years_above_and_below_normal(
        time_mode=time_mode,
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        month=month,
        season=season,
        percentages_of_normal=tuple(
            float(percent) for percent in percentages_of_normal.split(",") if percent
        ),
    ).to_json()
