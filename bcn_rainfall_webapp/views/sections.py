import plotly.express as px
import plotly.io
from flask import Blueprint, render_template

from bcn_rainfall_webapp import BEGIN_YEAR, END_YEAR, NORMAL_YEAR, api_client, db_client
from bcn_rainfall_webapp.utils.graph import (
    aggregate_plotly_json_figures,
    aggregate_plotly_json_pie_charts,
    sorted_vertical_bars_by_y_values,
)

sections = Blueprint(
    "navbar", __name__, static_folder="static", template_folder="templates"
)


@sections.route("/rainfall_by_year")
def rainfall_by_year():
    rainfall_by_year_as_plotly_json_list = []
    for cluster_count in [None, 2, 3, 4]:
        if (
            rainfall_by_year_as_plotly_json
            := db_client.get_rainfall_by_year_as_plotly_json(
                time_mode="yearly",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                plot_average=True,
                kmeans_cluster_count=cluster_count,
            )
        ):
            rainfall_by_year_as_plotly_json_list.append(rainfall_by_year_as_plotly_json)
        else:
            figure = plotly.io.from_json(
                api_client.get_rainfall_by_year_as_plotly_json(
                    time_mode="yearly",
                    begin_year=BEGIN_YEAR,
                    end_year=END_YEAR,
                    plot_average=True,
                    kmeans_cluster_count=cluster_count,
                )
            )
            figure.update_layout(
                colorway=px.colors.carto.Pastel[::2],
                title=f"Rainfall from {BEGIN_YEAR} to {END_YEAR}",
                xaxis={"title": None},
                yaxis={"title_standoff": 5},
            )

            data = figure.to_json()

            db_client.set_rainfall_by_year_as_plotly_json(
                time_mode="yearly",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
                plot_average=True,
                kmeans_cluster_count=cluster_count,
            )

            rainfall_by_year_as_plotly_json_list.append(data)

    monthly_rainfall_by_year_as_plotly_json_list = []
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
        if (
            monthly_rainfall_by_year_as_plotly_json
            := db_client.get_rainfall_by_year_as_plotly_json(
                time_mode="monthly",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                month=month,
            )
        ):
            monthly_rainfall_by_year_as_plotly_json_list.append(
                monthly_rainfall_by_year_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_by_year_as_plotly_json(
                time_mode="monthly",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                month=month,
            )

            db_client.set_rainfall_by_year_as_plotly_json(
                time_mode="monthly",
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
                month=month,
            )

            monthly_rainfall_by_year_as_plotly_json_list.append(data)

    fig_monthly_rainfalls = aggregate_plotly_json_figures(
        monthly_rainfall_by_year_as_plotly_json_list,
        layout={
            "title": f"Rainfall from {BEGIN_YEAR} to {END_YEAR} for each month",
            "yaxis": {"title": "Rainfall (mm)", "title_standoff": 5},
            "barmode": "stack",
            "colorway": px.colors.cyclical.IceFire[1:],
        },
    )

    return render_template(
        "sections/rainfall_by_year.html",
        plotlyRainfallByYearJSONList=rainfall_by_year_as_plotly_json_list,
        plotlyMonthlyRainfallsListJSON=[
            fig_monthly_rainfalls.to_json(),
            sorted_vertical_bars_by_y_values(
                fig_monthly_rainfalls,
                descending=True,
            ).to_json(),
            sorted_vertical_bars_by_y_values(
                fig_monthly_rainfalls,
                descending=False,
            ).to_json(),
        ],
    )


@sections.route("/rainfall_average")
def rainfall_average():
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

    return render_template(
        "sections/rainfall_average.html",
        plotlyRainfallAverageJSON=aggregate_plotly_json_figures(
            rainfall_averages_as_plotly_json_list,
            layout={
                "title": f"Average rainfall from {BEGIN_YEAR} to {END_YEAR}",
                "yaxis": {"title": "Rainfall (mm)", "title_standoff": 5},
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        ).to_json(),
    )


@sections.route("/rainfall_relative_distance_to_normal")
def rainfall_relative_distance_to_normal():
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

    return render_template(
        "sections/rainfall_relative_distance_to_normal.html",
        plotlyRainfallRelativeDistance2NormalJSON=aggregate_plotly_json_figures(
            relative_distances_to_rainfall_normal_as_plotly_json_list,
            layout={
                "title": f"Relative distance to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal from {BEGIN_YEAR} to {END_YEAR}",
                "yaxis": {
                    "title": "Relative distance to normal (%)",
                    "title_standoff": 5,
                },
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        ).to_json(),
    )


@sections.route("/years_compared_to_normal")
def years_compared_to_normal():
    percentage_of_years_compared_to_normal_as_plotly_json_list: list[str] = []
    percentage_of_years_compared_to_normal_as_plotly_json_list_2: list[str] = []
    for season in ["spring", "summer", "fall", "winter"]:
        if (
            seasonal_percentage_of_years_compared_to_normal_as_plotly_json
            := db_client.get_percentage_of_years_compared_to_normal_as_plotly_json(
                time_mode="seasonal",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                season=season,
            )
        ):
            percentage_of_years_compared_to_normal_as_plotly_json_list.append(
                seasonal_percentage_of_years_compared_to_normal_as_plotly_json
            )
        else:
            data = api_client.get_percentage_of_years_above_and_below_normal_as_plotly_json(
                time_mode="seasonal",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                season=season,
            )

            db_client.set_percentage_of_years_compared_to_normal_as_plotly_json(
                time_mode="seasonal",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
                season=season,
            )

            percentage_of_years_compared_to_normal_as_plotly_json_list.append(data)

        if (
            seasonal_percentage_of_years_compared_to_normal_as_plotly_json_2
            := db_client.get_percentage_of_years_compared_to_normal_as_plotly_json(
                time_mode="seasonal",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                season=season,
                percentages_of_normal="0,75,90,110,125,inf",
            )
        ):
            percentage_of_years_compared_to_normal_as_plotly_json_list_2.append(
                seasonal_percentage_of_years_compared_to_normal_as_plotly_json_2
            )
        else:
            data = api_client.get_percentage_of_years_above_and_below_normal_as_plotly_json(
                time_mode="seasonal",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                season=season,
                percentages_of_normal="0,75,90,110,125,inf",
            )

            db_client.set_percentage_of_years_compared_to_normal_as_plotly_json(
                time_mode="seasonal",
                normal_year=NORMAL_YEAR,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
                season=season,
                percentages_of_normal="0,75,90,110,125,inf",
            )

            percentage_of_years_compared_to_normal_as_plotly_json_list_2.append(data)

    if (
        percentage_of_years_above_and_below_normal_as_plotly_json
        := db_client.get_percentage_of_years_compared_to_normal_as_plotly_json(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
    ):
        pass
    else:
        data = api_client.get_percentage_of_years_above_and_below_normal_as_plotly_json(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )

        db_client.set_percentage_of_years_compared_to_normal_as_plotly_json(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            data=data,
        )

        percentage_of_years_above_and_below_normal_as_plotly_json = data

    if (
        percentage_of_years_above_and_below_normal_2_as_plotly_json
        := db_client.get_percentage_of_years_compared_to_normal_as_plotly_json(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            percentages_of_normal="0,75,90,110,125,inf",
        )
    ):
        pass
    else:
        data = api_client.get_percentage_of_years_above_and_below_normal_as_plotly_json(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            percentages_of_normal="0,75,90,110,125,inf",
        )

        db_client.set_percentage_of_years_compared_to_normal_as_plotly_json(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            data=data,
            percentages_of_normal="0,75,90,110,125,inf",
        )

        percentage_of_years_above_and_below_normal_2_as_plotly_json = data

    return render_template(
        "sections/years_compared_to_normal.html",
        plotlyYearsAboveNormalSeasonalJSON=aggregate_plotly_json_pie_charts(
            percentage_of_years_compared_to_normal_as_plotly_json_list,
            rows=2,
            cols=2,
            layout={
                "title": f"Years compared to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal for each season from {BEGIN_YEAR} to {END_YEAR}",
            },
            graph_labels=[
                "Spring",
                "Summer",
                "Fall",
                "Winter",
            ],
        ).to_json(),
        plotlyYearsAboveNormalSeasonal2JSON=aggregate_plotly_json_pie_charts(
            percentage_of_years_compared_to_normal_as_plotly_json_list_2,
            rows=2,
            cols=2,
            layout={
                "title": f"Years compared to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal for each season from {BEGIN_YEAR} to {END_YEAR}",
            },
            graph_labels=[
                "Spring",
                "Summer",
                "Fall",
                "Winter",
            ],
        ).to_json(),
        plotlyYearsAboveNormalJSON=percentage_of_years_above_and_below_normal_as_plotly_json,
        plotlyYearsAboveNormal2JSON=percentage_of_years_above_and_below_normal_2_as_plotly_json,
    )


@sections.route("/rainfall_standard_deviation")
def rainfall_standard_deviation():
    rainfall_standard_deviations_as_plotly_json_list: list[str] = []
    rainfall_standard_deviations_weighted_as_plotly_json_list: list[str] = []
    for time_mode in ["monthly", "seasonal"]:
        if (
            rainfall_standard_deviations_as_plotly_json
            := db_client.get_rainfall_standard_deviations_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )
        ):
            rainfall_standard_deviations_as_plotly_json_list.append(
                rainfall_standard_deviations_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_standard_deviations_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
            )

            db_client.set_rainfall_standard_deviations_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
            )

            rainfall_standard_deviations_as_plotly_json_list.append(data)

        if (
            rainfall_standard_deviations_weighted_as_plotly_json
            := db_client.get_rainfall_standard_deviations_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                weigh_by_average=True,
            )
        ):
            rainfall_standard_deviations_weighted_as_plotly_json_list.append(
                rainfall_standard_deviations_weighted_as_plotly_json
            )
        else:
            data = api_client.get_rainfall_standard_deviations_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                weigh_by_average=True,
            )

            db_client.set_rainfall_standard_deviations_as_plotly_json(
                time_mode=time_mode,
                begin_year=BEGIN_YEAR,
                end_year=END_YEAR,
                data=data,
                weigh_by_average=True,
            )

            rainfall_standard_deviations_weighted_as_plotly_json_list.append(data)

    return render_template(
        "sections/rainfall_standard_deviation.html",
        plotlyRainfallStandardDeviationJSON=aggregate_plotly_json_figures(
            rainfall_standard_deviations_as_plotly_json_list,
            layout={
                "title": f"Standard deviation from {BEGIN_YEAR} to {END_YEAR}",
                "yaxis": {"title": "Standard deviation (mm)", "title_standoff": 5},
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        ).to_json(),
        plotlyRainfallStandardDeviationWeightedJSON=aggregate_plotly_json_figures(
            rainfall_standard_deviations_weighted_as_plotly_json_list,
            layout={
                "title": f"Standard deviation weighted by average from {BEGIN_YEAR} to {END_YEAR}",
                "yaxis": {
                    "title": "Standard deviation weighted by average (%)",
                    "title_standoff": 5,
                },
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        ).to_json(),
    )
