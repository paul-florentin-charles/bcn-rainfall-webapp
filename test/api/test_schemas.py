from bcn_rainfall_core.utils import Month, Season, TimeMode

from bcn_rainfall_webapp.api.schemas import (
    APIQueryBegin,
    APIQueryBeginEnd,
    APIQueryBeginEndMonthSeason,
    APIQueryBeginEndMonthSeasonPlotAveragePlotLinearRegressionKmeans,
    APIQueryBeginEndMonthSeasonWeighByAverage,
    APIQueryBeginEndWeighByAverage,
    APIQueryBeginMonthSeason,
    APIQueryNormalBeginEnd,
    APIQueryNormalBeginEndMonthSeason,
    APIQueryNormalBeginEndMonthSeasonPercentagesOfNormal,
)


def test_api_query_begin():
    query = APIQueryBegin(time_mode=TimeMode.YEARLY, begin_year=2000)

    assert query.time_mode == TimeMode.YEARLY
    assert query.begin_year == 2000


def test_api_query_begin_end():
    query = APIQueryBeginEnd(time_mode=TimeMode.YEARLY, begin_year=2000, end_year=2001)

    assert query.time_mode == TimeMode.YEARLY
    assert query.begin_year == 2000
    assert query.end_year == 2001


def test_api_query_begin_month_season():
    query = APIQueryBeginMonthSeason(time_mode=TimeMode.YEARLY, begin_year=2000)

    assert query.time_mode == TimeMode.YEARLY
    assert query.begin_year == 2000
    assert query.month is None
    assert query.season is None


def test_api_query_normal_begin_end():
    query = APIQueryNormalBeginEnd(
        time_mode=TimeMode.YEARLY, normal_year=2000, begin_year=2001, end_year=2002
    )

    assert query.time_mode == TimeMode.YEARLY
    assert query.normal_year == 2000
    assert query.begin_year == 2001
    assert query.end_year == 2002


def test_api_query_begin_end_weigh_by_average():
    query = APIQueryBeginEndWeighByAverage(
        time_mode=TimeMode.YEARLY, begin_year=2000, end_year=2001, weigh_by_average=True
    )

    assert query.time_mode == TimeMode.YEARLY
    assert query.begin_year == 2000
    assert query.end_year == 2001
    assert query.weigh_by_average is True


def test_api_query_begin_end_month_season():
    query = APIQueryBeginEndMonthSeason(
        time_mode=TimeMode.YEARLY, begin_year=2000, end_year=2001
    )

    assert query.time_mode == TimeMode.YEARLY
    assert query.begin_year == 2000
    assert query.end_year == 2001
    assert query.month is None
    assert query.season is None


def test_api_query_normal_begin_end_month_season():
    query = APIQueryNormalBeginEndMonthSeason(
        time_mode=TimeMode.SEASONAL,
        normal_year=2000,
        begin_year=2001,
        end_year=2002,
        season=Season.WINTER,
    )

    assert query.time_mode == TimeMode.SEASONAL
    assert query.normal_year == 2000
    assert query.begin_year == 2001
    assert query.end_year == 2002
    assert query.month is None
    assert query.season == Season.WINTER


def test_api_query_begin_end_month_season_weigh_by_average():
    query = APIQueryBeginEndMonthSeasonWeighByAverage(
        time_mode=TimeMode.MONTHLY,
        begin_year=2000,
        end_year=2001,
        weigh_by_average=True,
        month=Month.JANUARY,
    )

    assert query.time_mode == TimeMode.MONTHLY
    assert query.begin_year == 2000
    assert query.end_year == 2001
    assert query.weigh_by_average is True
    assert query.month == Month.JANUARY
    assert query.season is None


def test_api_query_begin_end_month_season_plot_average_plot_linear_regression_kmeans():
    query = APIQueryBeginEndMonthSeasonPlotAveragePlotLinearRegressionKmeans(
        time_mode=TimeMode.YEARLY,
        begin_year=2000,
        end_year=2001,
        plot_average=True,
        plot_linear_regression=True,
        kmeans_cluster_count=2,
    )

    assert query.time_mode == TimeMode.YEARLY
    assert query.begin_year == 2000
    assert query.end_year == 2001
    assert query.plot_average is True
    assert query.plot_linear_regression is True
    assert query.kmeans_cluster_count == 2


def test_api_query_normal_begin_end_month_season_percentages_of_normal():
    query = APIQueryNormalBeginEndMonthSeasonPercentagesOfNormal(
        time_mode=TimeMode.MONTHLY,
        normal_year=2000,
        begin_year=2001,
        end_year=2002,
        percentages_of_normal="0,100",
        month=Month.JUNE,
    )

    assert query.time_mode == TimeMode.MONTHLY
    assert query.normal_year == 2000
    assert query.begin_year == 2001
    assert query.end_year == 2002
    assert query.percentages_of_normal == "0,100"
    assert query.month == Month.JUNE
    assert query.season is None
