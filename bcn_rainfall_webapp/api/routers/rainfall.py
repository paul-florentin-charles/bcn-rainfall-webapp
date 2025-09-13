from bcn_rainfall_core.utils import TimeMode
from flask_openapi3 import APIBlueprint, Tag

from bcn_rainfall_webapp.api import MAX_YEAR_AVAILABLE, bcn_rainfall
from bcn_rainfall_webapp.api.schemas import (
    APIQueryBeginEndMonthSeason,
    APIQueryBeginEndMonthSeasonWeighByAverage,
    APIQueryBeginMonthSeason,
    APIQueryNormalBeginEndMonthSeason,
)
from bcn_rainfall_webapp.api.utils import (
    RainfallModel,
    raise_time_mode_error_or_do_nothing,
    raise_year_related_error_or_do_nothing,
)

rainfall_blueprint = APIBlueprint(
    "rainfall", __name__, url_prefix="/rainfall", abp_tags=[Tag(name="Rainfall")]
)


@rainfall_blueprint.get(
    "/average",
    summary="Retrieve rainfall average for Barcelona between two years.",
    description=f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={"200": RainfallModel},
)
def get_rainfall_average(query: APIQueryBeginEndMonthSeason):
    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)
    raise_time_mode_error_or_do_nothing(query.time_mode, query.month, query.season)

    rainfall_average = bcn_rainfall.get_rainfall_average(
        query.time_mode,
        begin_year=query.begin_year,
        end_year=query.end_year,
        month=query.month,
        season=query.season,
    )

    return RainfallModel(
        name="rainfall average (mm)",
        value=rainfall_average,  # type: ignore
        begin_year=query.begin_year,
        end_year=query.end_year,
        time_mode=query.time_mode,
        month=query.month if query.time_mode == TimeMode.MONTHLY else None,
        season=query.season if query.time_mode == TimeMode.SEASONAL else None,
    ).model_dump(mode="json")


@rainfall_blueprint.get(
    "/normal",
    summary="Retrieve 30 years rainfall average for Barcelona after a given year.",
    description="Commonly called rainfall normal.",
    responses={"200": RainfallModel},
)
def get_rainfall_normal(query: APIQueryBeginMonthSeason):
    raise_time_mode_error_or_do_nothing(query.time_mode, query.month, query.season)

    normal = bcn_rainfall.get_normal(
        query.time_mode,
        begin_year=query.begin_year,
        month=query.month,
        season=query.season,
    )

    return RainfallModel(
        name="rainfall normal (mm)",
        value=normal,  # type: ignore
        begin_year=query.begin_year,
        end_year=query.begin_year + 29,
        time_mode=query.time_mode,
        month=query.month if query.time_mode == TimeMode.MONTHLY else None,
        season=query.season if query.time_mode == TimeMode.SEASONAL else None,
    ).model_dump(mode="json")


@rainfall_blueprint.get(
    "/relative_distance_to_normal",
    summary="Retrieve the rainfall relative distance to normal for Barcelona between two years.",
    description="The metric is a percentage that can be negative. <br>"
    "Its formula is `(average - normal) / normal * 100`. <br> "
    "1. `average` is average rainfall computed between `begin_year` and `end_year`<br>"
    "2. `normal` is normal rainfall computed from `normal_year`<br>"
    "If 100%, average is twice the normal. <br>"
    "If -50%, average is half the normal. <br>"
    f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={"200": RainfallModel},
)
def get_rainfall_relative_distance_to_normal(
    query: APIQueryNormalBeginEndMonthSeason,
):
    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)
    raise_time_mode_error_or_do_nothing(query.time_mode, query.month, query.season)

    relative_distance_to_normal = bcn_rainfall.get_relative_distance_to_normal(
        query.time_mode,
        normal_year=query.normal_year,
        begin_year=query.begin_year,
        end_year=query.end_year,
        month=query.month,
        season=query.season,
    )

    return RainfallModel(
        name="relative distance to rainfall normal (%)",
        value=relative_distance_to_normal,  # type: ignore
        normal_year=query.normal_year,
        begin_year=query.begin_year,
        end_year=query.end_year,
        time_mode=query.time_mode,
        month=query.month if query.time_mode == TimeMode.MONTHLY else None,
        season=query.season if query.time_mode == TimeMode.SEASONAL else None,
    ).model_dump(mode="json")


@rainfall_blueprint.get(
    "/standard_deviation",
    summary="Compute the standard deviation of rainfall for Barcelona between two years.",
    description=f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={"200": RainfallModel},
)
def get_rainfall_standard_deviation(
    query: APIQueryBeginEndMonthSeasonWeighByAverage,
):
    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)
    raise_time_mode_error_or_do_nothing(query.time_mode, query.month, query.season)

    rainfall_standard_deviation = bcn_rainfall.get_rainfall_standard_deviation(
        query.time_mode,
        begin_year=query.begin_year,
        end_year=query.end_year,
        month=query.month,
        season=query.season,
        weigh_by_average=query.weigh_by_average,
    )

    return RainfallModel(
        name=f"rainfall standard deviation {'weighted by average' if query.weigh_by_average else '(mm)'}",
        value=rainfall_standard_deviation,  # type: ignore
        begin_year=query.begin_year,
        end_year=query.end_year,
        time_mode=query.time_mode,
        month=query.month if query.time_mode == TimeMode.MONTHLY else None,
        season=query.season if query.time_mode == TimeMode.SEASONAL else None,
    ).model_dump(mode="json")
