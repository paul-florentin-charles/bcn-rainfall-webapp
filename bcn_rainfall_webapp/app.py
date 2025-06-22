"""
Webapp run with Flask that communicates with an API (FastAPI/Uvicorn) to display rainfall-related data.
Work-in-progress!
"""

from flask import Flask, render_template

from bcn_rainfall_webapp import BEGIN_YEAR, END_YEAR, NORMAL_YEAR, api_client
from bcn_rainfall_webapp.utils.graph import aggregate_plotly_json_figures
from bcn_rainfall_webapp.views import navbar

flask_app = Flask(__name__)
flask_app.register_blueprint(navbar)


@flask_app.route("/")
def index():
    seasonal_rainfalls = []
    for season in ["spring", "summer", "fall", "winter"]:
        seasonal_rainfalls.append(
            api_client.get_rainfall_by_year_as_plotly_json(
                time_mode="seasonal",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                season=season,
            )
        )

    fig_seasonal_rainfalls = aggregate_plotly_json_figures(
        seasonal_rainfalls,
        layout={
            "title": f"Rainfall (mm) between {BEGIN_YEAR} and {END_YEAR} for each season",
            "yaxis": {"title": "Rainfall (mm)"},
            "barmode": "stack",
        },
    )

    ## Averages ##

    monthly_averages = api_client.get_rainfall_averages_as_plotly_json(
        time_mode="monthly",
        begin_year=BEGIN_YEAR,
        end_year=END_YEAR,
    )

    seasonal_averages = api_client.get_rainfall_averages_as_plotly_json(
        time_mode="seasonal",
        begin_year=BEGIN_YEAR,
        end_year=END_YEAR,
    )

    fig_averages = aggregate_plotly_json_figures(
        [monthly_averages, seasonal_averages],
        layout={
            "title": f"Average rainfall (mm) between {BEGIN_YEAR} and {END_YEAR}",
            "yaxis": {"title": "Rainfall (mm)"},
        },
    )

    ## LinReg slopes ##

    monthly_linreg_slopes = api_client.get_rainfall_linreg_slopes_as_plotly_json(
        time_mode="monthly",
        begin_year=BEGIN_YEAR,
        end_year=END_YEAR,
    )

    seasonal_linreg_slopes = api_client.get_rainfall_linreg_slopes_as_plotly_json(
        time_mode="seasonal",
        begin_year=BEGIN_YEAR,
        end_year=END_YEAR,
    )

    fig_linreg_slopes = aggregate_plotly_json_figures(
        [monthly_linreg_slopes, seasonal_linreg_slopes],
        layout={
            "title": f"Average linear regression slope (mm/year) between {BEGIN_YEAR} and {END_YEAR}",
            "yaxis": {"title": "Linear regression slope (mm/year)"},
        },
    )

    ## Relative distances to normal ##

    monthly_relative_distances_to_normal = (
        api_client.get_rainfall_relative_distances_to_normal_as_plotly_json(
            time_mode="monthly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
    )

    seasonal_relative_distances_to_normal = (
        api_client.get_rainfall_relative_distances_to_normal_as_plotly_json(
            time_mode="seasonal",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
    )

    fig_relative_distances_to_normal = aggregate_plotly_json_figures(
        [monthly_relative_distances_to_normal, seasonal_relative_distances_to_normal],
        layout={
            "title": f"Relative distance to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal (%) between {BEGIN_YEAR} and {END_YEAR}",
            "yaxis": {"title": "Relative distance to normal (%)"},
        },
    )

    return render_template(
        "index.html",
        plotlySeasonalRainfallsJSON=fig_seasonal_rainfalls,
        plotlyAveragesJSON=fig_averages,
        plotlyLinRegJSON=fig_linreg_slopes,
        plotlyRelativeDistance2NormalJSON=fig_relative_distances_to_normal,
    )
