from bcn_rainfall_core.utils import Month, Season, TimeMode
from pydantic import BaseModel, Field


class RainfallModel(BaseModel):
    """
    Model for depicting a value linked to rainfall data.
    It could be either a float value for a rainfall value, a percentage, etc. or an integer value for years.
    """

    name: str
    value: float | int
    begin_year: int
    end_year: int
    normal_year: int | None = None
    time_mode: TimeMode = TimeMode.YEARLY
    month: Month | None = None
    season: Season | None = None


class APISettings(BaseModel):
    """Type definition for API settings: FastAPI settings & Uvicorn server settings."""

    class FastAPISettings(BaseModel):
        """Type definition for FastAPI settings."""

        root_path: str
        title: str
        summary: str | None = Field(None)
        debug: bool | None = Field(None)

    class APIServerSettings(BaseModel):
        """Type definition for Uvicorn server settings."""

        host: str
        port: int
        reload: bool | None = Field(None)

    fastapi: FastAPISettings
    server: APIServerSettings
