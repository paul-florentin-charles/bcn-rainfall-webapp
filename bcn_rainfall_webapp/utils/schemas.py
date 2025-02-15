from pydantic import BaseModel, Field


class WebappServerSettings(BaseModel):
    """Type definition for Flask server settings."""

    host: str
    port: int
    debug: bool | None = Field(None)
