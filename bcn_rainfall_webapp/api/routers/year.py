from bcn_rainfall_core.utils import TimeMode
from flask_openapi3 import APIBlueprint, Tag

from bcn_rainfall_webapp.api import MAX_YEAR_AVAILABLE, bcn_rainfall
from bcn_rainfall_webapp.api.schemas import APIQueryNormalBeginEndMonthSeason
from bcn_rainfall_webapp.api.utils import (
    RainfallModel,
    raise_time_mode_error_or_do_nothing,
    raise_year_related_error_or_do_nothing,
)

year_blueprint = APIBlueprint(
    "year", __name__, url_prefix="/year", abp_tags=[Tag(name="Year")]
)


@year_blueprint.get(
    "/below_normal",
    summary="Compute the number of years below normal for a specific year range.",
    description="Normal is computed as a 30 years average "
    f"starting from the year set via normal_year. <br>"
    f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={"200": RainfallModel},
)
def get_years_below_normal(
    query: APIQueryNormalBeginEndMonthSeason,
):
    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)
    raise_time_mode_error_or_do_nothing(query.time_mode, query.month, query.season)

    years_below_normal = bcn_rainfall.get_years_below_normal(
        query.time_mode,
        normal_year=query.normal_year,
        begin_year=query.begin_year,
        end_year=query.end_year,
        month=query.month,
        season=query.season,
    )

    return RainfallModel(
        name="years below rainfall normal",
        value=years_below_normal,
        normal_year=query.normal_year,
        begin_year=query.begin_year,
        end_year=query.end_year,
        time_mode=query.time_mode,
        month=query.month if query.time_mode == TimeMode.MONTHLY else None,
        season=query.season if query.time_mode == TimeMode.SEASONAL else None,
    ).model_dump(mode="json")


@year_blueprint.get(
    "/above_normal",
    summary="Compute the number of years above normal for a specific year range.",
    description="Normal is computed as a 30 years average "
    f"starting from the year set via normal_year. <br>"
    f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={"200": RainfallModel},
)
def get_years_above_normal(
    query: APIQueryNormalBeginEndMonthSeason,
):
    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)
    raise_time_mode_error_or_do_nothing(query.time_mode, query.month, query.season)

    years_above_normal = bcn_rainfall.get_years_above_normal(
        query.time_mode,
        normal_year=query.normal_year,
        begin_year=query.begin_year,
        end_year=query.end_year,
        month=query.month,
        season=query.season,
    )

    return RainfallModel(
        name="years above rainfall normal",
        value=years_above_normal,
        normal_year=query.normal_year,
        begin_year=query.begin_year,
        end_year=query.end_year,
        time_mode=query.time_mode,
        month=query.month if query.time_mode == TimeMode.MONTHLY else None,
        season=query.season if query.time_mode == TimeMode.SEASONAL else None,
    ).model_dump(mode="json")
