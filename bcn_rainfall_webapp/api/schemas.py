from bcn_rainfall_core.utils import Month, Season, TimeMode
from pydantic import BaseModel, Field

from bcn_rainfall_webapp.api import MAX_YEAR_AVAILABLE, MIN_YEAR_AVAILABLE


class APIQueryParameters(BaseModel):
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
    month: Month | None = Field(None, description="Month filter")
    season: Season | None = Field(None, description="Season filter")


class APIQueryParametersWithNormal(BaseModel):
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
    month: Month | None = Field(None, description="Month filter")
    season: Season | None = Field(None, description="Season filter")
