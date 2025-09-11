from pydantic import BaseModel, Field


class DevelopmentServerSettings(BaseModel):
    """Type definition for Flask server settings."""

    host: str
    port: int
    debug: bool | None = Field(default=None)


class ProductionServerSettings(BaseModel):
    """Type definition for Waitress server settings."""

    host: str
    port: int


class RedisServerSettings(BaseModel):
    """Type definition for Redis server settings."""

    host: str
    port: int
    db: int = Field(default=0)
    decode_responses: bool = Field(default=True)


class APISettings(BaseModel):
    """Type definition for API settings"""

    root_path: str
    title: str
    summary: str | None = Field(None)
