from flask import Blueprint, jsonify, render_template

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
        rainfall_by_year_list.append(
            api_client.get_rainfall_by_year_as_plotly_json(
                time_mode="yearly",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                plot_average=True,
                kmeans_cluster_count=cluster_count,
            )
        )

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
        },
    )

    return render_template(
        "sections/rainfall_by_year.html",
        plotlyRainfallByYearJSONList=rainfall_by_year_list,
        plotlyMonthlyRainfallsJSON=fig_monthly_rainfalls,
    )


@navbar.route("/rainfall_average")
def rainfall_average():
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
            "title": f"Average rainfall between {BEGIN_YEAR} and {END_YEAR}",
            "yaxis": {"title": "Rainfall (mm)"},
        },
    )

    return render_template(
        "sections/rainfall_average.html",
        plotlyRainfallAverageJSON=fig_averages,
    )


@navbar.route("/rainfall_normal")
def rainfall_normal():
    return jsonify(
        api_client.get_rainfall_normal(
            time_mode="monthly", begin_year=BEGIN_YEAR, month="May"
        )
    )


@navbar.route("/rainfall_relative_distance_to_normal")
def rainfall_relative_distance_to_normal():
    return render_template(
        "sections/rainfall_relative_distance_to_normal.html",
        plotlyRainfallRelativeDistance2NormalJSON=api_client.get_rainfall_relative_distances_to_normal_as_plotly_json(
            time_mode="monthly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        ),
    )


@navbar.route("/years_below_normal")
def years_below_normal():
    return jsonify(
        api_client.get_years_below_normal(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
    )


@navbar.route("/years_above_normal")
def years_above_normal():
    years_compared_to_normal_season_list = []
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

    return render_template(
        "sections/years_above_normal.html",
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
        plotlyYearsAboveNormalJSON2=api_client.get_percentage_of_years_above_and_below_normal_as_plotly_json(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        ),
    )


@navbar.route("/rainfall_standard_deviation")
def rainfall_standard_deviation():
    fig_monthly = api_client.get_rainfall_standard_deviations_as_plotly_json(
        time_mode="monthly",
        begin_year=BEGIN_YEAR,
        end_year=END_YEAR,
    )
    fig_seasonal = api_client.get_rainfall_standard_deviations_as_plotly_json(
        time_mode="seasonal",
        begin_year=BEGIN_YEAR,
        end_year=END_YEAR,
    )

    fig_monthly_weighted = api_client.get_rainfall_standard_deviations_as_plotly_json(
        time_mode="monthly",
        begin_year=BEGIN_YEAR,
        end_year=END_YEAR,
        weigh_by_average=True,
    )
    fig_seasonal_weighted = api_client.get_rainfall_standard_deviations_as_plotly_json(
        time_mode="seasonal",
        begin_year=BEGIN_YEAR,
        end_year=END_YEAR,
        weigh_by_average=True,
    )

    return render_template(
        "sections/rainfall_standard_deviation.html",
        plotlyRainfallStandardDeviationJSON=aggregate_plotly_json_figures(
            [fig_monthly, fig_seasonal],
            layout={
                "title": f"Standard deviation between {BEGIN_YEAR} and {END_YEAR}",
                "yaxis": {"title": "Standard deviation (mm)"},
            },
        ),
        plotlyRainfallStandardDeviationWeightedJSON=aggregate_plotly_json_figures(
            [fig_monthly_weighted, fig_seasonal_weighted],
            layout={
                "title": f"Standard deviation weighted by average between {BEGIN_YEAR} and {END_YEAR}",
                "yaxis": {
                    "title": "Standard deviation weighted by average (%)",
                },
            },
        ),
    )
