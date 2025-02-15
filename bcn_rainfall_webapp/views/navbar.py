from flask import Blueprint, jsonify, render_template

from bcn_rainfall_webapp import BEGIN_YEAR, END_YEAR, NORMAL_YEAR, api_client

navbar = Blueprint(
    "navbar", __name__, static_folder="static", template_folder="templates"
)


@navbar.route("/rainfall_average")
def rainfall_average():
    return render_template(
        "sections/rainfall_average.html",
        plotlyRainfallAverageJSON=api_client.get_rainfall_by_year_as_plotly_json(
            time_mode="yearly",
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            plot_average=True,
        ),
        plotlyRainfallAverageJSON2=api_client.get_rainfall_by_year_as_plotly_json(
            time_mode="seasonal",
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            plot_average=True,
            plot_linear_regression=True,
            season="winter",
        ),
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
    return render_template(
        "sections/years_above_normal.html",
        plotlyYearsAboveNormalJSON=api_client.get_percentage_of_years_above_and_below_normal_as_plotly_json(
            time_mode="seasonal",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            season="fall",
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
    return jsonify(
        api_client.get_rainfall_standard_deviation(
            time_mode="seasonal",
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            season="winter",
            weigh_by_average=True,
        )
    )
