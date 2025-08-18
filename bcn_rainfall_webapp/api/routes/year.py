from typing import Annotated

from bcn_rainfall_core.utils import Month, Season, TimeMode
from fastapi import Query

import bcn_rainfall_webapp.api.utils.errors as http_err
from bcn_rainfall_webapp.api.routes import (
    MAX_NORMAL_YEAR_AVAILABLE,
    MAX_YEAR_AVAILABLE,
    MIN_YEAR_AVAILABLE,
    all_rainfall,
)
from bcn_rainfall_webapp.api.utils import (
    RainfallModel,
)


async def get_years_below_normal(
    time_mode: TimeMode,
    normal_year: Annotated[
        int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_NORMAL_YEAR_AVAILABLE)
    ],
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    http_err.raise_year_related_error_or_do_nothing(begin_year, end_year)
    http_err.raise_time_mode_error_or_do_nothing(time_mode, month, season)

    years_below_normal = all_rainfall.get_years_below_normal(
        time_mode,
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        month=month,
        season=season,
    )

    return RainfallModel(
        name="years below rainfall normal",
        value=years_below_normal,  # type: ignore
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


async def get_years_above_normal(
    time_mode: TimeMode,
    normal_year: Annotated[
        int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_NORMAL_YEAR_AVAILABLE)
    ],
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    http_err.raise_year_related_error_or_do_nothing(begin_year, end_year)
    http_err.raise_time_mode_error_or_do_nothing(time_mode, month, season)

    years_above_normal = all_rainfall.get_years_above_normal(
        time_mode,
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        month=month,
        season=season,
    )

    return RainfallModel(
        name="years above rainfall normal",
        value=years_above_normal,  # type: ignore
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )
