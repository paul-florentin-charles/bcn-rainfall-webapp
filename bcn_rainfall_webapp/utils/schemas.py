from pydantic import BaseModel, Field


class WebappServerSettings(BaseModel):
    """Type definition for Flask server settings."""

    host: str
    port: int
    debug: bool | None = Field(default=None)


class RedisServerSettings(BaseModel):
    """Type definition for Redis server settings."""

    host: str
    port: int
    db: int = Field(default=0)
    decode_responses: bool = Field(default=True)
