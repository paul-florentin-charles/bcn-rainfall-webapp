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
from bcn_rainfall_webapp.utils.graph import aggregate_plotly_json_figures
from bcn_rainfall_webapp.views import sections

flask_app = Flask(__name__)
flask_app.register_blueprint(sections)


@flask_app.route("/")
def index():
    ctx_variables_dict: dict[str, Any] = {}

    seasonal_rainfall_as_plotly_json_list: list[str] = []
    for season in ["spring", "summer", "fall", "winter"]:
        if (
            seasonal_rainfall_as_plotly_json
            := db_client.get_seasonal_rainfall_as_plotly_json(
                season=season,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )
        ):
            seasonal_rainfall_as_plotly_json_list.append(
                seasonal_rainfall_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_by_year_as_plotly_json(
                time_mode="seasonal",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                season=season,
            )

            db_client.set_seasonal_rainfall_as_plotly_json(
                season=season,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
            )

            seasonal_rainfall_as_plotly_json_list.append(data)

    ctx_variables_dict["plotlySeasonalRainfallsJSON"] = aggregate_plotly_json_figures(
        seasonal_rainfall_as_plotly_json_list,
        layout={
            "title": f"Rainfall between {BEGIN_YEAR} and {END_YEAR} for each season",
            "xaxis": {"title": "Year"},
            "yaxis": {"title": "Rainfall (mm)"},
            "barmode": "stack",
            "colorway": ["#3bd330", "#cfe23d", "#ce9a30", "#4d8bae"],
        },
    )

    ## Averages ##

    rainfall_averages_as_plotly_json_list: list[str] = []
    for time_mode in ["monthly", "seasonal"]:
        if (
            rainfall_averages_as_plotly_json
            := db_client.get_rainfall_averages_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )
        ):
            rainfall_averages_as_plotly_json_list.append(
                rainfall_averages_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_averages_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )

            db_client.set_rainfall_averages_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
            )

            rainfall_averages_as_plotly_json_list.append(data)

    ctx_variables_dict["plotlyAveragesJSON"] = aggregate_plotly_json_figures(
        rainfall_averages_as_plotly_json_list,
        layout={
            "title": f"Average rainfall between {BEGIN_YEAR} and {END_YEAR}",
            "yaxis": {"title": "Rainfall (mm)"},
            "colorway": ["#5bd0d1", "#cb7e5c"],
        },
    )

    ## LinReg slopes ##

    rainfall_linreg_slopes_as_plotly_json_list: list[str] = []
    for time_mode in ["monthly", "seasonal"]:
        if (
            rainfall_linreg_slopes_as_plotly_json
            := db_client.get_rainfall_linreg_slopes_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )
        ):
            rainfall_linreg_slopes_as_plotly_json_list.append(
                rainfall_linreg_slopes_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_linreg_slopes_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )

            db_client.set_rainfall_linreg_slopes_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
            )

            rainfall_linreg_slopes_as_plotly_json_list.append(data)

    ctx_variables_dict["plotlyLinRegJSON"] = aggregate_plotly_json_figures(
        rainfall_linreg_slopes_as_plotly_json_list,
        layout={
            "title": f"Average linear regression slope between {BEGIN_YEAR} and {END_YEAR}",
            "yaxis": {"title": "Linear regression slope (mm/year)"},
            "colorway": ["#5bd0d1", "#cb7e5c"],
        },
    )

    ## Relative distances to normal ##

    relative_distances_to_rainfall_normal_as_plotly_json_list: list[str] = []
    for time_mode in ["monthly", "seasonal"]:
        if (
            relative_distances_to_rainfall_normal_as_plotly_json
            := db_client.get_relative_distances_to_rainfall_normal_as_plotly_json(
                time_mode=time_mode,
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )
        ):
            relative_distances_to_rainfall_normal_as_plotly_json_list.append(
                relative_distances_to_rainfall_normal_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_relative_distances_to_normal_as_plotly_json(
                time_mode=time_mode,
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )

            db_client.set_relative_distances_to_rainfall_normal_as_plotly_json(
                time_mode=time_mode,
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
            )

            relative_distances_to_rainfall_normal_as_plotly_json_list.append(data)

    ctx_variables_dict["plotlyRelativeDistance2NormalJSON"] = (
        aggregate_plotly_json_figures(
            relative_distances_to_rainfall_normal_as_plotly_json_list,
            layout={
                "title": f"Relative distance to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal between {BEGIN_YEAR} and {END_YEAR}",
                "yaxis": {"title": "Relative distance to normal (%)"},
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        )
    )

    return render_template(
        "index.html",
        **ctx_variables_dict,
    )
