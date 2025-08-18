from typing import Annotated

from bcn_rainfall_core.utils import Month, Season, TimeMode
from fastapi import Query
from starlette.responses import StreamingResponse

import bcn_rainfall_webapp.api.utils.errors as http_err
from bcn_rainfall_webapp.api.routes import (
    MAX_YEAR_AVAILABLE,
    MIN_YEAR_AVAILABLE,
    all_rainfall,
)


def get_rainfall_by_year_as_csv(
    time_mode: TimeMode,
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

    csv_str = all_rainfall.export_as_csv(
        time_mode,
        begin_year=begin_year,
        end_year=end_year,
        month=month,
        season=season,
    )

    filename = f"rainfall_{begin_year}_{end_year}"
    if time_mode == TimeMode.MONTHLY:
        filename = f"{filename}_{month.value}"  # type: ignore
    elif time_mode == TimeMode.SEASONAL:
        filename = f"{filename}_{season.value}"  # type: ignore

    return StreamingResponse(
        iter(csv_str),
        headers={"Content-Disposition": f'inline; filename="{filename}.csv"'},
        media_type="text/csv",
    )
