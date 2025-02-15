"""
Webapp run with Flask that communicates with an API (FastAPI/Uvicorn) to display rainfall-related data.
Work-in-progress!
"""

from typing import Any

import plotly.graph_objs as go
import plotly.io
from flask import Flask, render_template

from bcn_rainfall_webapp import BEGIN_YEAR, END_YEAR, NORMAL_YEAR, api_client
from bcn_rainfall_webapp.views import navbar

flask_app = Flask(__name__)
flask_app.register_blueprint(navbar)


def _aggregate_traces_json_as_figure(
    traces_json: list[str], *, layout: dict[str, Any] | None = None
) -> go.Figure:
    figure = go.Figure()
    for trace_json in traces_json:
        figure.add_traces(list(plotly.io.from_json(trace_json).select_traces()))

    figure.update_layout(
        legend={
            "yanchor": "top",
            "y": 0.99,
            "xanchor": "left",
            "x": 0.01,
            "bgcolor": "rgba(125, 125, 125, 0.7)",
        },
        font={
            "color": "white",
            "family": "Khula, sans-serif",
            "size": 11,
        },
        paper_bgcolor="rgba(34, 34, 34, 0.6)",
        plot_bgcolor="rgba(123, 104, 75, 0.3)",
        margin={"t": 65, "r": 65, "b": 70, "l": 75},
        autosize=True,
        **(layout or {}),
    )

    return figure


@flask_app.route("/")
def index():
    summer_rainfall = api_client.get_rainfall_by_year_as_plotly_json(
        time_mode="seasonal",
        begin_year=BEGIN_YEAR,
        end_year=END_YEAR,
        season="summer",
        plot_average=True,
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

    fig_averages = _aggregate_traces_json_as_figure(
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

    fig_linreg_slopes = _aggregate_traces_json_as_figure(
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

    fig_relative_distances_to_normal = _aggregate_traces_json_as_figure(
        [monthly_relative_distances_to_normal, seasonal_relative_distances_to_normal],
        layout={
            "title": f"Relative distance to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal (%) between {BEGIN_YEAR} and {END_YEAR}",
            "yaxis": {"title": "Relative distance to normal (%)"},
        },
    )

    return render_template(
        "index.html",
        plotlySummerRainfallJSON=summer_rainfall,
        plotlyAveragesJSON=fig_averages.to_json(),
        plotlyLinRegJSON=fig_linreg_slopes.to_json(),
        plotlyRelativeDistance2NormalJSON=fig_relative_distances_to_normal.to_json(),
    )
