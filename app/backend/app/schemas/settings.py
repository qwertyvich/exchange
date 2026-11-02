from pydantic import BaseModel, Field


class SettingsRead(BaseModel):
    global_api_id: int | None = None
    global_api_hash_masked: str | None = None
    default_online_ping_minutes: int = 5
    default_online_ping_interval: int = 300
    message_rate_limit_per_minute: int = 5


class SettingsUpdate(BaseModel):
    global_api_id: int | None = None
    global_api_hash: str | None = Field(default=None, max_length=512)
    default_online_ping_minutes: int | None = Field(default=None, ge=1)
    default_online_ping_interval: int | None = Field(default=None, ge=30)
    message_rate_limit_per_minute: int | None = Field(default=None, ge=1, le=60)
