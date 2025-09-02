from bcn_rainfall_core.utils import TimeMode
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from bcn_rainfall_webapp.api import MAX_YEAR_AVAILABLE, all_rainfall
from bcn_rainfall_webapp.api.schemas import APIQueryParameters
from bcn_rainfall_webapp.api.utils import (
    raise_time_mode_error_or_do_nothing,
    raise_year_related_error_or_do_nothing,
)

csv_blueprint = APIBlueprint(
    "csv", __name__, url_prefix="/csv", abp_tags=[Tag(name="CSV")]
)


@csv_blueprint.get(
    "/rainfall_by_year",
    summary="Retrieve CSV of rainfall by year data: ['Year', 'Rainfall'] columns.",
    description="Could either be for rainfall upon a whole year, a specific month or a given season.<br>"
    f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
    responses={
        "200": {
            "content": {"text/csv": {"schema": {"type": "string", "format": "binary"}}},
            "description": "CSV of rainfall by year",
        }
    },
)
def get_rainfall_by_year_as_csv(query: APIQueryParameters):
    if query.end_year is None:
        query.end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(query.begin_year, query.end_year)
    raise_time_mode_error_or_do_nothing(query.time_mode, query.month, query.season)

    csv_str = all_rainfall.export_as_csv(
        query.time_mode,
        begin_year=query.begin_year,
        end_year=query.end_year,
        month=query.month,
        season=query.season,
    )

    filename = f"rainfall_{query.begin_year}_{query.end_year}"
    if query.time_mode == TimeMode.MONTHLY:
        filename = f"{filename}_{query.month.value}"  # type: ignore
    elif query.time_mode == TimeMode.SEASONAL:
        filename = f"{filename}_{query.season.value}"  # type: ignore

    # Return as streaming response
    return Response(
        csv_str,
        mimetype="text/csv",
        headers={"Content-Disposition": f'inline; filename="{filename}.csv"'},
    )
