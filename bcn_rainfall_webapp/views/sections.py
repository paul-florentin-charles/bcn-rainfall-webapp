from typing import Any

import plotly.express as px
import plotly.io
from bcn_rainfall_core.utils import Month, Season, TimeMode
from flask import Blueprint, render_template

import bcn_rainfall_webapp.api.routers.graph as graphs
import bcn_rainfall_webapp.api.schemas as api_schemas
from bcn_rainfall_webapp import (
    BEGIN_YEAR,
    END_YEAR,
    NORMAL_YEAR,
    db_client,
)
from bcn_rainfall_webapp.utils.graph import (
    DEFAULT_LAYOUT,
    aggregate_plotly_json_figures,
    aggregate_plotly_json_pie_charts,
    sorted_vertical_bars_by_y_values,
)

webapp_blueprint = Blueprint(
    "webapp", __name__, static_folder="static", template_folder="templates"
)


@webapp_blueprint.route("/")
def index():
    ctx_variables_dict: dict[str, Any] = {}

    seasonal_rainfall_as_plotly_json_list: list[str] = []
    for season in Season:
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
            data = graphs.get_rainfall_by_year_as_plotly_json(
                api_schemas.APIQueryBeginEndMonthSeasonPlotAveragePlotLinearRegressionKmeans(
                    **parameters, time_mode=TimeMode.SEASONAL
                ),
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
    for time_mode in [TimeMode.MONTHLY, TimeMode.SEASONAL]:
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
            data = graphs.get_rainfall_averages_as_plotly_json(
                api_schemas.APIQueryBeginEnd(**parameters),
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
    for time_mode in [TimeMode.MONTHLY, TimeMode.SEASONAL]:
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
            data = graphs.get_rainfall_linreg_slopes_as_plotly_json(
                api_schemas.APIQueryBeginEnd(**parameters),
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
    for time_mode in [TimeMode.MONTHLY, TimeMode.SEASONAL]:
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
            data = graphs.get_relative_distances_to_rainfall_normal_as_plotly_json(
                api_schemas.APIQueryNormalBeginEnd(**parameters),
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
        title="Home - BCN Rainfall",
        **ctx_variables_dict,
    )


@webapp_blueprint.route("/rainfall_by_year")
def rainfall_by_year():
    rainfall_by_year_as_plotly_json_list = []
    for cluster_count in [None, 2, 3, 4]:
        parameters = dict(
            time_mode=TimeMode.YEARLY,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            plot_average=True,
            kmeans_cluster_count=cluster_count,
        )
        if (
            rainfall_by_year_as_plotly_json
            := db_client.get_rainfall_by_year_as_plotly_json(
                **parameters,
            )
        ):
            rainfall_by_year_as_plotly_json_list.append(rainfall_by_year_as_plotly_json)
        else:
            figure = plotly.io.from_json(
                graphs.get_rainfall_by_year_as_plotly_json(
                    api_schemas.APIQueryBeginEndMonthSeasonPlotAveragePlotLinearRegressionKmeans(
                        **parameters
                    ),
                )
            )
            figure.update_layout(
                **DEFAULT_LAYOUT,
                colorway=px.colors.carto.Pastel[::2],
                title=f"Rainfall from {BEGIN_YEAR} to {END_YEAR}",
                xaxis={"title": None, "rangeslider_visible": True},
                yaxis={"title_standoff": 5},
            )

            data = figure.to_json()

            db_client.set_rainfall_by_year_as_plotly_json(
                **parameters,
                data=data,
            )

            rainfall_by_year_as_plotly_json_list.append(data)

    monthly_rainfall_by_year_as_plotly_json_list = []
    for month in Month.values():
        parameters = dict(
            time_mode=TimeMode.MONTHLY,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            month=month,
        )
        if (
            monthly_rainfall_by_year_as_plotly_json
            := db_client.get_rainfall_by_year_as_plotly_json(
                **parameters,
            )
        ):
            monthly_rainfall_by_year_as_plotly_json_list.append(
                monthly_rainfall_by_year_as_plotly_json
            )
        else:
            data = graphs.get_rainfall_by_year_as_plotly_json(
                api_schemas.APIQueryBeginEndMonthSeasonPlotAveragePlotLinearRegressionKmeans(
                    **parameters
                ),
            )

            db_client.set_rainfall_by_year_as_plotly_json(
                **parameters,
                data=data,
            )

            monthly_rainfall_by_year_as_plotly_json_list.append(data)

    fig_monthly_rainfalls = aggregate_plotly_json_figures(
        monthly_rainfall_by_year_as_plotly_json_list,
        layout={
            "title": f"Rainfall from {BEGIN_YEAR} to {END_YEAR} for each month",
            "yaxis": {"title": "Rainfall (mm)", "title_standoff": 5},
            "barmode": "stack",
            "colorway": px.colors.sequential.Turbo,
        },
    )

    return render_template(
        "sections/rainfall_by_year.html",
        title="Rainfall by year - BCN Rainfall",
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


@webapp_blueprint.route("/rainfall_average")
def rainfall_average():
    rainfall_averages_as_plotly_json_list: list[str] = []
    for time_mode in [TimeMode.MONTHLY, TimeMode.SEASONAL]:
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
            data = graphs.get_rainfall_averages_as_plotly_json(
                api_schemas.APIQueryBeginEnd(**parameters),
            )

            db_client.set_rainfall_averages_as_plotly_json(
                **parameters,
                data=data,
            )

            rainfall_averages_as_plotly_json_list.append(data)

    return render_template(
        "sections/rainfall_average.html",
        title="Rainfall average - BCN Rainfall",
        plotlyRainfallAverageJSON=aggregate_plotly_json_figures(
            rainfall_averages_as_plotly_json_list,
            layout={
                "title": f"Average rainfall from {BEGIN_YEAR} to {END_YEAR}",
                "yaxis": {"title": "Rainfall (mm)", "title_standoff": 5},
                "colorway": ["#5bd0d1", "#cb7e5c"],
            },
        ).to_json(),
    )


@webapp_blueprint.route("/rainfall_relative_distance_to_normal")
def rainfall_relative_distance_to_normal():
    relative_distances_to_rainfall_normal_as_plotly_json_list: list[str] = []
    for time_mode in [TimeMode.MONTHLY, TimeMode.SEASONAL]:
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
            data = graphs.get_relative_distances_to_rainfall_normal_as_plotly_json(
                api_schemas.APIQueryNormalBeginEnd(**parameters),
            )

            db_client.set_relative_distances_to_rainfall_normal_as_plotly_json(
                **parameters,
                data=data,
            )

            relative_distances_to_rainfall_normal_as_plotly_json_list.append(data)

    return render_template(
        "sections/rainfall_relative_distance_to_normal.html",
        title="Relative distance to normal - BCN Rainfall",
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


@webapp_blueprint.route("/years_compared_to_normal")
def years_compared_to_normal():
    percentage_of_years_compared_to_normal_as_plotly_json_list: list[str] = []
    percentage_of_years_compared_to_normal_as_plotly_json_list_2: list[str] = []
    for season in Season.values():
        parameters = dict(
            time_mode=TimeMode.SEASONAL,
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            season=season,
        )
        if (
            seasonal_percentage_of_years_compared_to_normal_as_plotly_json
            := db_client.get_percentage_of_years_compared_to_normal_as_plotly_json(
                **parameters,
            )
        ):
            percentage_of_years_compared_to_normal_as_plotly_json_list.append(
                seasonal_percentage_of_years_compared_to_normal_as_plotly_json
            )
        else:
            data = graphs.get_percentage_of_years_above_and_below_normal_as_plotly_json(
                api_schemas.APIQueryNormalBeginEndMonthSeasonPercentagesOfNormal(
                    **parameters
                ),
            )

            db_client.set_percentage_of_years_compared_to_normal_as_plotly_json(
                **parameters,
                data=data,
            )

            percentage_of_years_compared_to_normal_as_plotly_json_list.append(data)

        if (
            seasonal_percentage_of_years_compared_to_normal_as_plotly_json_2
            := db_client.get_percentage_of_years_compared_to_normal_as_plotly_json(
                **parameters,
                percentages_of_normal="0,75,90,110,125,inf",
            )
        ):
            percentage_of_years_compared_to_normal_as_plotly_json_list_2.append(
                seasonal_percentage_of_years_compared_to_normal_as_plotly_json_2
            )
        else:
            data = graphs.get_percentage_of_years_above_and_below_normal_as_plotly_json(
                api_schemas.APIQueryNormalBeginEndMonthSeasonPercentagesOfNormal(
                    **parameters, percentages_of_normal="0,75,90,110,125,inf"
                ),
            )

            db_client.set_percentage_of_years_compared_to_normal_as_plotly_json(
                **parameters,
                data=data,
                percentages_of_normal="0,75,90,110,125,inf",
            )

            percentage_of_years_compared_to_normal_as_plotly_json_list_2.append(data)

    plotly_data_ctx_dict: dict[str, str] = {}
    for key, percentages_of_normal in [
        ("plotlyYearsAboveNormalJSON", "0,80,120,inf"),
        ("plotlyYearsAboveNormal2JSON", "0,75,90,110,125,inf"),
    ]:
        parameters = dict(
            time_mode=TimeMode.YEARLY,
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            percentages_of_normal=percentages_of_normal,
        )

        if (
            db_data
            := db_client.get_percentage_of_years_compared_to_normal_as_plotly_json(
                **parameters,
            )
        ):
            plotly_data_ctx_dict[key] = db_data
        else:
            data = graphs.get_percentage_of_years_above_and_below_normal_as_plotly_json(
                api_schemas.APIQueryNormalBeginEndMonthSeasonPercentagesOfNormal(
                    **parameters
                ),
            )

            figure = plotly.io.from_json(data)
            figure.update_layout(
                **DEFAULT_LAYOUT,
            )
            data = figure.to_json()

            db_client.set_percentage_of_years_compared_to_normal_as_plotly_json(
                **parameters,
                data=data,
            )

            plotly_data_ctx_dict[key] = data

    return render_template(
        "sections/years_compared_to_normal.html",
        title="Years compared to normal - BCN Rainfall",
        plotlyYearsAboveNormalSeasonalJSON=aggregate_plotly_json_pie_charts(
            percentage_of_years_compared_to_normal_as_plotly_json_list,
            rows=2,
            cols=2,
            layout={
                "title": f"Years compared to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal for each season from {BEGIN_YEAR} to {END_YEAR}",
            },
            graph_labels=[season.capitalize() for season in Season.values()],
        ).to_json(),
        plotlyYearsAboveNormalSeasonal2JSON=aggregate_plotly_json_pie_charts(
            percentage_of_years_compared_to_normal_as_plotly_json_list_2,
            rows=2,
            cols=2,
            layout={
                "title": f"Years compared to {NORMAL_YEAR}-{NORMAL_YEAR + 29} normal for each season from {BEGIN_YEAR} to {END_YEAR}",
            },
            graph_labels=[season.capitalize() for season in Season.values()],
        ).to_json(),
        **plotly_data_ctx_dict,
    )


@webapp_blueprint.route("/rainfall_standard_deviation")
def rainfall_standard_deviation():
    rainfall_standard_deviations_as_plotly_json_list: list[str] = []
    rainfall_standard_deviations_weighted_as_plotly_json_list: list[str] = []
    for time_mode in [TimeMode.MONTHLY, TimeMode.SEASONAL]:
        parameters = dict(
            time_mode=time_mode,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
        if (
            rainfall_standard_deviations_as_plotly_json
            := db_client.get_rainfall_standard_deviations_as_plotly_json(
                **parameters,
            )
        ):
            rainfall_standard_deviations_as_plotly_json_list.append(
                rainfall_standard_deviations_as_plotly_json
            )
        else:
            data = graphs.get_rainfall_standard_deviations_as_plotly_json(
                api_schemas.APIQueryBeginEndWeighByAverage(**parameters),
            )

            db_client.set_rainfall_standard_deviations_as_plotly_json(
                **parameters,
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
            data = graphs.get_rainfall_standard_deviations_as_plotly_json(
                api_schemas.APIQueryBeginEndWeighByAverage(
                    **parameters,
                    weigh_by_average=True,
                )
            )

            db_client.set_rainfall_standard_deviations_as_plotly_json(
                **parameters,
                data=data,
                weigh_by_average=True,
            )

            rainfall_standard_deviations_weighted_as_plotly_json_list.append(data)

    return render_template(
        "sections/rainfall_standard_deviation.html",
        title="Standard deviation - BCN Rainfall",
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
