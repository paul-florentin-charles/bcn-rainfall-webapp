import plotly.express as px
import plotly.io
from flask import Blueprint, render_template

from bcn_rainfall_webapp import BEGIN_YEAR, END_YEAR, NORMAL_YEAR, api_client
from bcn_rainfall_webapp.utils.graph import (
    aggregate_plotly_json_figures,
    aggregate_plotly_json_pie_charts,
)

navbar = Blueprint(
    "navbar", __name__, static_folder="static", template_folder="templates"
)


@navbar.route("/rainfall_by_year")
def rainfall_by_year():
    rainfall_by_year_list = []
    for cluster_count in [None, 2, 3]:
        fig = plotly.io.from_json(
            api_client.get_rainfall_by_year_as_plotly_json(
                time_mode="yearly",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                plot_average=True,
                kmeans_cluster_count=cluster_count,
            )
        )
        fig.update_layout(
            colorway=["#5bd0d1", "#b15bd1", "#c3d15b", "#d15b7e"],
        )

        rainfall_by_year_list.append(fig.to_json())

    monthly_rainfalls = []
    for month in [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]:
        monthly_rainfalls.append(
            api_client.get_rainfall_by_year_as_plotly_json(
                time_mode="monthly",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                month=month,
            )
        )

    fig_monthly_rainfalls = aggregate_plotly_json_figures(
        monthly_rainfalls,
        layout={
            "title": f"Rainfall between {BEGIN_YEAR} and {END_YEAR} for each month",
            "xaxis": {"title": "Year"},
            "yaxis": {"title": "Rainfall (mm)"},
            "barmode": "stack",
            "colorway": px.colors.cyclical.IceFire[1:],
        },
    )

    return render_template(
        "sections/rainfall_by_year.html",
        plotlyRainfallByYearJSONList=rainfall_by_year_list,
        plotlyMonthlyRainfallsJSON=fig_monthly_rainfalls,
    )


@navbar.route("/rainfall_average")
def rainfall_average():
    fig_averages = aggregate_plotly_json_figures(
        [
            api_client.get_rainfall_averages_as_plotly_json(
                time_mode="monthly",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            ),
            api_client.get_rainfall_averages_as_plotly_json(
                time_mode="seasonal",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            ),
        ],
        layout={
            "title": f"Average rainfall between {BEGIN_YEAR} and {END_YEAR}",
            "yaxis": {"title": "Rainfall (mm)"},
            "colorway": ["#5bd0d1", "#cb7e5c"],
        },
    )

    return render_template(
        "sections/rainfall_average.html",
        plotlyRainfallAverageJSON=fig_averages,
    )


@navbar.route("/rainfall_relative_distance_to_normal")
def rainfall_relative_distance_to_normal():
    fig_rainfall_relative_distances_to_normal = aggregate_plotly_json_figures(
        [
            api_client.get_rainfall_relative_distances_to_normal_as_plotly_json(
                time_mode="monthly",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            ),
            api_client.get_rainfall_relative_distances_to_normal_as_plotly_json(
                time_mode="seasonal",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            ),
        ],
        layout={
            "title": f"Rainfall relative distance to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal between {BEGIN_YEAR} and {END_YEAR}",
            "yaxis": {"title": "Relative distance to normal (%)"},
            "colorway": ["#5bd0d1", "#cb7e5c"],
        },
    )

    return render_template(
        "sections/rainfall_relative_distance_to_normal.html",
        plotlyRainfallRelativeDistance2NormalJSON=fig_rainfall_relative_distances_to_normal,
    )


@navbar.route("/years_compared_to_normal")
def years_compared_to_normal():
    years_compared_to_normal_season_list = []
    years_compared_to_normal_season_list_2 = []
    for season in ["spring", "summer", "fall", "winter"]:
        years_compared_to_normal_season_list.append(
            api_client.get_percentage_of_years_above_and_below_normal_as_plotly_json(
                time_mode="seasonal",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                season=season,
            )
        )

        years_compared_to_normal_season_list_2.append(
            api_client.get_percentage_of_years_above_and_below_normal_as_plotly_json(
                time_mode="seasonal",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                season=season,
                percentages_of_normal="0,75,90,110,125,inf",
            )
        )

    return render_template(
        "sections/years_compared_to_normal.html",
        plotlyYearsAboveNormalSeasonalJSON=aggregate_plotly_json_pie_charts(
            years_compared_to_normal_season_list,
            rows=2,
            cols=2,
            layout={
                "title": f"Years compared to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal for each season between {BEGIN_YEAR} and {END_YEAR}",
            },
            graph_labels=[
                "Spring",
                "Summer",
                "Fall",
                "Winter",
            ],
        ),
        plotlyYearsAboveNormalSeasonal2JSON=aggregate_plotly_json_pie_charts(
            years_compared_to_normal_season_list_2,
            rows=2,
            cols=2,
            layout={
                "title": f"Years compared to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal for each season between {BEGIN_YEAR} and {END_YEAR}",
            },
            graph_labels=[
                "Spring",
                "Summer",
                "Fall",
                "Winter",
            ],
        ),
        plotlyYearsAboveNormalJSON=api_client.get_percentage_of_years_above_and_below_normal_as_plotly_json(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        ),
    )


@navbar.route("/rainfall_standard_deviation")
def rainfall_standard_deviation():
    traces_json: list[str] = []
    traces_weighted_json: list[str] = []
    for time_mode in ["monthly", "seasonal"]:
        traces_json.append(
            api_client.get_rainfall_standard_deviations_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )
        )

        traces_weighted_json.append(
            api_client.get_rainfall_standard_deviations_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                weigh_by_average=True,
            )
        )

    return render_template(
        "sections/rainfall_standard_deviation.html",
        plotlyRainfallStandardDeviationJSON=aggregate_plotly_json_figures(
            traces_json,
            layout={
                "title": f"Standard deviation between {BEGIN_YEAR} and {END_YEAR}",
                "yaxis": {"title": "Standard deviation (mm)"},
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        ),
        plotlyRainfallStandardDeviationWeightedJSON=aggregate_plotly_json_figures(
            traces_weighted_json,
            layout={
                "title": f"Standard deviation weighted by average between {BEGIN_YEAR} and {END_YEAR}",
                "yaxis": {
                    "title": "Standard deviation weighted by average (%)",
                },
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        ),
    )
