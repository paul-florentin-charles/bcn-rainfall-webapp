from bcn_rainfall_core.utils import Month, Season, TimeMode
from pydantic import BaseModel

from bcn_rainfall_webapp.api.query_parameters import (
    get_pydantic_field,
)

## -- 1st level schemas (extend BaseModel) -- ##


class APIQueryBegin(BaseModel):
    time_mode: TimeMode = get_pydantic_field("time_mode")
    begin_year: int = get_pydantic_field("begin_year")


class APIQueryNormalBeginEnd(BaseModel):
    time_mode: TimeMode = get_pydantic_field("time_mode")
    normal_year: int = get_pydantic_field("normal_year")
    begin_year: int = get_pydantic_field("begin_year")
    end_year: int | None = get_pydantic_field("end_year")


## -- 2nd level schemas (extend 1st level schemas) -- ##


class APIQueryBeginEnd(APIQueryBegin):
    end_year: int | None = get_pydantic_field("end_year")


class APIQueryBeginMonthSeason(APIQueryBegin):
    month: Month | None = get_pydantic_field("month")
    season: Season | None = get_pydantic_field("season")


class APIQueryNormalBeginEndMonthSeason(APIQueryNormalBeginEnd):
    month: Month | None = get_pydantic_field("month")
    season: Season | None = get_pydantic_field("season")


## -- 3rd level schemas (extend 2nd level schemas) -- ##


class APIQueryBeginEndWeighByAverage(APIQueryBeginEnd):
    weigh_by_average: bool = get_pydantic_field("weigh_by_average")


class APIQueryBeginEndMonthSeason(APIQueryBeginEnd):
    month: Month | None = get_pydantic_field("month")
    season: Season | None = get_pydantic_field("season")


class APIQueryNormalBeginEndMonthSeasonPercentagesOfNormal(
    APIQueryNormalBeginEndMonthSeason
):
    percentages_of_normal: str = get_pydantic_field("percentages_of_normal")


## -- 4th level schemas (extend 3rd level schemas) -- ##


class APIQueryBeginEndMonthSeasonWeighByAverage(APIQueryBeginEndMonthSeason):
    weigh_by_average: bool = get_pydantic_field("weigh_by_average")


class APIQueryBeginEndMonthSeasonPlotAveragePlotLinearRegressionKmeans(
    APIQueryBeginEndMonthSeason
):
    plot_average: bool = get_pydantic_field("plot_average")
    plot_linear_regression: bool = get_pydantic_field("plot_linear_regression")
    kmeans_cluster_count: int | None = get_pydantic_field("kmeans_cluster_count")
