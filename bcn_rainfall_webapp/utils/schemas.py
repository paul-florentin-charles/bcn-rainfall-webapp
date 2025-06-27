from pydantic import BaseModel, Field


class WebappServerSettings(BaseModel):
    """Type definition for Flask server settings."""

    host: str
    port: int
    debug: bool | None = Field(None)


class RedisServerSettings(BaseModel):
    """Type definition for Redis server settings."""

    host: str
    port: int
    db: int = Field(0)
    decode_responses: bool = Field(True)
