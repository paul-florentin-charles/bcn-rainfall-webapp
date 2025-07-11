"""
Webapp run with Flask that communicates with an API (FastAPI/Uvicorn) to display rainfall-related data.
Work-in-progress!
"""

from typing import Any

from flask import Flask, render_template

from bcn_rainfall_webapp import (
    BEGIN_YEAR,
    END_YEAR,
    NORMAL_YEAR,
    api_client,
    db_client,
)
from bcn_rainfall_webapp.utils import SEASONS
from bcn_rainfall_webapp.utils.graph import (
    aggregate_plotly_json_figures,
    sorted_vertical_bars_by_y_values,
)
from bcn_rainfall_webapp.views import sections

flask_app = Flask(__name__)
flask_app.register_blueprint(sections)


@flask_app.route("/")
def index():
    ctx_variables_dict: dict[str, Any] = {}

    seasonal_rainfall_as_plotly_json_list: list[str] = []
    for season in SEASONS:
        parameters = dict(
            season=season,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
        if (
            seasonal_rainfall_as_plotly_json
            := db_client.get_seasonal_rainfall_as_plotly_json(
                **parameters,
            )
        ):
            seasonal_rainfall_as_plotly_json_list.append(
                seasonal_rainfall_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_by_year_as_plotly_json(
                **parameters,
                time_mode="seasonal",
            )

            db_client.set_seasonal_rainfall_as_plotly_json(
                **parameters,
                data=data,
            )

            seasonal_rainfall_as_plotly_json_list.append(data)

    seasonal_rainfalls_by_year = aggregate_plotly_json_figures(
        seasonal_rainfall_as_plotly_json_list,
        layout={
            "title": f"Rainfall from {BEGIN_YEAR} to {END_YEAR} for each season",
            "xaxis": {"rangeslider_visible": True},
            "yaxis": {"title": "Rainfall (mm)", "title_standoff": 5},
            "barmode": "stack",
            "colorway": ["#32a326", "#c4d63a", "#c97632", "#4d8bae"],
        },
    )

    ctx_variables_dict["plotlySeasonalRainfallsListJSON"] = [
        seasonal_rainfalls_by_year.to_json(),
        sorted_vertical_bars_by_y_values(
            seasonal_rainfalls_by_year,
            descending=True,
        ).to_json(),
        sorted_vertical_bars_by_y_values(
            seasonal_rainfalls_by_year,
            descending=False,
        ).to_json(),
    ]

    ## Averages ##

    rainfall_averages_as_plotly_json_list: list[str] = []
    for time_mode in ["monthly", "seasonal"]:
        parameters = dict(
            time_mode=time_mode,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
        if (
            rainfall_averages_as_plotly_json
            := db_client.get_rainfall_averages_as_plotly_json(
                **parameters,
            )
        ):
            rainfall_averages_as_plotly_json_list.append(
                rainfall_averages_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_averages_as_plotly_json(
                **parameters,
            )

            db_client.set_rainfall_averages_as_plotly_json(
                **parameters,
                data=data,
            )

            rainfall_averages_as_plotly_json_list.append(data)

    ctx_variables_dict["plotlyAveragesJSON"] = aggregate_plotly_json_figures(
        rainfall_averages_as_plotly_json_list,
        layout={
            "title": f"Average rainfall from {BEGIN_YEAR} to {END_YEAR}",
            "yaxis": {"title": "Rainfall (mm)", "title_standoff": 5},
            "colorway": ["#5bd0d1", "#cb7e5c"],
        },
    ).to_json()

    ## LinReg slopes ##

    rainfall_linreg_slopes_as_plotly_json_list: list[str] = []
    for time_mode in ["monthly", "seasonal"]:
        parameters = dict(
            time_mode=time_mode,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
        if (
            rainfall_linreg_slopes_as_plotly_json
            := db_client.get_rainfall_linreg_slopes_as_plotly_json(
                **parameters,
            )
        ):
            rainfall_linreg_slopes_as_plotly_json_list.append(
                rainfall_linreg_slopes_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_linreg_slopes_as_plotly_json(
                **parameters,
            )

            db_client.set_rainfall_linreg_slopes_as_plotly_json(
                **parameters,
                data=data,
            )

            rainfall_linreg_slopes_as_plotly_json_list.append(data)

    ctx_variables_dict["plotlyLinRegJSON"] = aggregate_plotly_json_figures(
        rainfall_linreg_slopes_as_plotly_json_list,
        layout={
            "title": f"Average linear regression slope from {BEGIN_YEAR} to {END_YEAR}",
            "yaxis": {
                "title": "Linear regression slope (mm/year)",
                "title_standoff": 5,
            },
            "colorway": ["#5bd0d1", "#cb7e5c"],
        },
    ).to_json()

    ## Relative distances to normal ##

    relative_distances_to_rainfall_normal_as_plotly_json_list: list[str] = []
    for time_mode in ["monthly", "seasonal"]:
        parameters = dict(
            time_mode=time_mode,
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
        if (
            relative_distances_to_rainfall_normal_as_plotly_json
            := db_client.get_relative_distances_to_rainfall_normal_as_plotly_json(
                **parameters,
            )
        ):
            relative_distances_to_rainfall_normal_as_plotly_json_list.append(
                relative_distances_to_rainfall_normal_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_relative_distances_to_normal_as_plotly_json(
                **parameters,
            )

            db_client.set_relative_distances_to_rainfall_normal_as_plotly_json(
                **parameters,
                data=data,
            )

            relative_distances_to_rainfall_normal_as_plotly_json_list.append(data)

    ctx_variables_dict["plotlyRelativeDistance2NormalJSON"] = (
        aggregate_plotly_json_figures(
            relative_distances_to_rainfall_normal_as_plotly_json_list,
            layout={
                "title": f"Relative distance to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal from {BEGIN_YEAR} to {END_YEAR}",
                "yaxis": {
                    "title": "Relative distance to normal (%)",
                    "title_standoff": 5,
                },
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        )
    ).to_json()

    return render_template(
        "index.html",
        **ctx_variables_dict,
    )
