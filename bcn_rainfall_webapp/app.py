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
    redis_client,
)
from bcn_rainfall_webapp.utils.graph import aggregate_plotly_json_figures
from bcn_rainfall_webapp.views import navbar

flask_app = Flask(__name__)
flask_app.register_blueprint(navbar)


@flask_app.route("/")
def index():
    ctx_variables_dict: dict[str, Any] = {}

    if seasonal_rainfalls_as_plotly_json := redis_client.get(
        "seasonal_rainfalls_as_plotly_json"
    ):
        ctx_variables_dict["plotlySeasonalRainfallsJSON"] = (
            seasonal_rainfalls_as_plotly_json
        )
    else:
        seasonal_rainfalls_as_plotly_json = aggregate_plotly_json_figures(
            [
                api_client.get_rainfall_by_year_as_plotly_json(
                    time_mode="seasonal",
                    begin_year=BEGIN_YEAR,
                    end_year=END_YEAR,
                    season=season,
                )
                for season in ["spring", "summer", "fall", "winter"]
            ],
            layout={
                "title": f"Rainfall between {BEGIN_YEAR} and {END_YEAR} for each season",
                "xaxis": {"title": "Year"},
                "yaxis": {"title": "Rainfall (mm)"},
                "barmode": "stack",
                "colorway": ["#3bd330", "#cfe23d", "#ce9a30", "#4d8bae"],
            },
        )

        ctx_variables_dict["plotlySeasonalRainfallsJSON"] = (
            seasonal_rainfalls_as_plotly_json
        )
        redis_client.set(
            "seasonal_rainfalls_as_plotly_json", seasonal_rainfalls_as_plotly_json
        )

    ## Averages ##

    if rainfall_averages_as_plotly_json := redis_client.get(
        "rainfall_averages_as_plotly_json"
    ):
        ctx_variables_dict["plotlyAveragesJSON"] = rainfall_averages_as_plotly_json
    else:
        rainfall_averages_as_plotly_json = aggregate_plotly_json_figures(
            [
                api_client.get_rainfall_averages_as_plotly_json(
                    time_mode=time_mode,
                    begin_year=BEGIN_YEAR,
                    end_year=END_YEAR,
                )
                for time_mode in ["monthly", "seasonal"]
            ],
            layout={
                "title": f"Average rainfall between {BEGIN_YEAR} and {END_YEAR}",
                "yaxis": {"title": "Rainfall (mm)"},
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        )

        ctx_variables_dict["plotlyAveragesJSON"] = rainfall_averages_as_plotly_json
        redis_client.set(
            "rainfall_averages_as_plotly_json", rainfall_averages_as_plotly_json
        )

    ## LinReg slopes ##

    if linreg_slopes_as_plotly_json := redis_client.get("linreg_slopes_as_plotly_json"):
        ctx_variables_dict["plotlyLinRegJSON"] = linreg_slopes_as_plotly_json
    else:
        linreg_slopes_as_plotly_json = aggregate_plotly_json_figures(
            [
                api_client.get_rainfall_linreg_slopes_as_plotly_json(
                    time_mode=time_mode,
                    begin_year=BEGIN_YEAR,
                    end_year=END_YEAR,
                )
                for time_mode in ["monthly", "seasonal"]
            ],
            layout={
                "title": f"Average linear regression slope between {BEGIN_YEAR} and {END_YEAR}",
                "yaxis": {"title": "Linear regression slope (mm/year)"},
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        )

        ctx_variables_dict["plotlyLinRegJSON"] = linreg_slopes_as_plotly_json
        redis_client.set("linreg_slopes_as_plotly_json", linreg_slopes_as_plotly_json)

    ## Relative distances to normal ##

    if relative_distances_to_rainfall_normal_as_plotly_json := redis_client.get(
        "relative_distances_to_rainfall_normal_as_plotly_json"
    ):
        ctx_variables_dict["plotlyRelativeDistance2NormalJSON"] = (
            relative_distances_to_rainfall_normal_as_plotly_json
        )
    else:
        relative_distances_to_rainfall_normal_as_plotly_json = aggregate_plotly_json_figures(
            [
                api_client.get_rainfall_relative_distances_to_normal_as_plotly_json(
                    time_mode=time_mode,
                    normal_year=NORMAL_YEAR,
                    begin_year=BEGIN_YEAR,
                    end_year=END_YEAR,
                )
                for time_mode in ["monthly", "seasonal"]
            ],
            layout={
                "title": f"Relative distance to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal between {BEGIN_YEAR} and {END_YEAR}",
                "yaxis": {"title": "Relative distance to normal (%)"},
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        )

        ctx_variables_dict["plotlyRelativeDistance2NormalJSON"] = (
            relative_distances_to_rainfall_normal_as_plotly_json
        )
        redis_client.set(
            "relative_distances_to_rainfall_normal_as_plotly_json",
            relative_distances_to_rainfall_normal_as_plotly_json,
        )

    return render_template(
        "index.html",
        **ctx_variables_dict,
    )
