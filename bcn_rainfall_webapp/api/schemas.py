from bcn_rainfall_core.utils import Month, Season, TimeMode
from pydantic import BaseModel, Field

from bcn_rainfall_webapp.api import MAX_YEAR_AVAILABLE, MIN_YEAR_AVAILABLE


class APIQueryParametersMinimal(BaseModel):
    time_mode: TimeMode = Field(..., description="Time mode to filter by")
    begin_year: int = Field(
        ...,
        ge=MIN_YEAR_AVAILABLE,
        le=MAX_YEAR_AVAILABLE,
        description=f"Start year (>= {MIN_YEAR_AVAILABLE} and <= {MAX_YEAR_AVAILABLE})",
    )
    end_year: int | None = Field(
        None,
        ge=MIN_YEAR_AVAILABLE,
        le=MAX_YEAR_AVAILABLE,
        description=f"End year (>= {MIN_YEAR_AVAILABLE} and <= {MAX_YEAR_AVAILABLE})",
    )


class APIQueryParametersMinimalWithWeighByAverage(APIQueryParametersMinimal):
    weigh_by_average: bool = Field(False, description="Weigh metric by average")


class APIQueryParametersMinimalWithNormal(BaseModel):
    time_mode: TimeMode = Field(..., description="Time mode to filter by")
    normal_year: int = Field(
        ...,
        ge=MIN_YEAR_AVAILABLE,
        le=MAX_YEAR_AVAILABLE,
        description=f"Normal year (>= {MIN_YEAR_AVAILABLE} and <= {MAX_YEAR_AVAILABLE})",
    )
    begin_year: int = Field(
        ...,
        ge=MIN_YEAR_AVAILABLE,
        le=MAX_YEAR_AVAILABLE,
        description=f"Start year (>= {MIN_YEAR_AVAILABLE} and <= {MAX_YEAR_AVAILABLE})",
    )
    end_year: int | None = Field(
        None,
        ge=MIN_YEAR_AVAILABLE,
        le=MAX_YEAR_AVAILABLE,
        description=f"End year (>= {MIN_YEAR_AVAILABLE} and <= {MAX_YEAR_AVAILABLE})",
    )


class APIQueryParameters(APIQueryParametersMinimal):
    month: Month | None = Field(None, description="Month to filter by")
    season: Season | None = Field(None, description="Season to filter by")


class APIQueryParametersWithNormal(APIQueryParametersMinimalWithNormal):
    month: Month | None = Field(None, description="Month to filter by")
    season: Season | None = Field(None, description="Season to filter by")


class APIQueryParametersWithPercentagesOfNormal(APIQueryParametersWithNormal):
    percentages_of_normal: str = Field(
        "0,80,120,inf", description="Percentages of normal to split by (inf = infinity)"
    )


class APIQueryParametersWithoutEndYear(BaseModel):
    time_mode: TimeMode = Field(..., description="Time mode to filter by")
    begin_year: int = Field(
        ...,
        ge=MIN_YEAR_AVAILABLE,
        le=MAX_YEAR_AVAILABLE,
        description=f"Start year (>= {MIN_YEAR_AVAILABLE} and <= {MAX_YEAR_AVAILABLE})",
    )
    month: Month | None = Field(None, description="Month to filter by")
    season: Season | None = Field(None, description="Season to filter by")


class APIQueryParametersWithWeighByAverage(APIQueryParameters):
    weigh_by_average: bool = Field(False, description="Weigh by average")


class APIQueryParametersForRainfallByYear(APIQueryParameters):
    plot_average: bool = Field(False, description="Plot average")
    plot_linear_regression: bool = Field(False, description="Plot linear regression")
    kmeans_cluster_count: int | None = Field(
        None, ge=2, description="KMeans cluster count"
    )
