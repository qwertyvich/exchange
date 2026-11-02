from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


AccountStatusValue = Literal["imported", "active", "disabled", "error"]


class AccountCreate(BaseModel):
    phone_number: str | None = Field(default=None, max_length=64)
    name: str = Field(default="Manual account", min_length=1, max_length=160)
    display_name: str | None = Field(default=None, max_length=160)
    username: str | None = Field(default=None, max_length=160)
    geo: str | None = Field(default=None, max_length=80)
    session_file: str | None = Field(default=None, max_length=255)
    status: AccountStatusValue = "imported"
    online_keepalive: bool = False
    online_keepalive_enabled: bool = False
    online_ping_interval_minutes: int = Field(default=15, ge=15)
    proxy_id: int | None = None
    individual_api_id: int | None = None
    individual_api_hash: str | None = None
    api_id_override: int | None = None
    api_hash_override: str | None = None


class AccountUpdate(BaseModel):
    phone_number: str | None = Field(default=None, max_length=64)
    name: str | None = Field(default=None, min_length=1, max_length=160)
    display_name: str | None = Field(default=None, min_length=1, max_length=160)
    username: str | None = Field(default=None, max_length=160)
    geo: str | None = Field(default=None, max_length=80)
    status: AccountStatusValue | None = None
    online_keepalive: bool | None = None
    online_keepalive_enabled: bool | None = None
    online_ping_interval_minutes: int | None = Field(default=None, ge=15)
    proxy_id: int | None = None
    individual_api_id: int | None = None
    individual_api_hash: str | None = None
    api_id_override: int | None = None
    api_hash_override: str | None = None


class AccountCredentialsUpdate(BaseModel):
    individual_api_id: int | None = None
    individual_api_hash: str | None = Field(default=None, max_length=512)


class ScheduledPayload(BaseModel):
    schedule_for: datetime | None = None


class ChangeNamePayload(ScheduledPayload):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str | None = Field(default=None, max_length=80)


class ChangeUsernamePayload(ScheduledPayload):
    username: str = Field(min_length=1, max_length=160)


class ChangeBioPayload(ScheduledPayload):
    bio: str = Field(max_length=140)


class KeepaliveUpdate(BaseModel):
    online_keepalive_enabled: bool
    online_ping_interval_minutes: int = Field(ge=15)


class SendDialogMessagePayload(BaseModel):
    text: str = Field(min_length=1, max_length=4096)


class SendUsernameMessagePayload(BaseModel):
    username: str = Field(min_length=1, max_length=160)
    text: str = Field(min_length=1, max_length=4096)
    confirmed: bool = False


class AccountRead(BaseModel):
    id: int
    phone_number: str | None = None
    name: str
    display_name: str
    username: str | None = None
    geo: str | None = None
    session_file: str
    status: str
    online_keepalive: bool
    online_keepalive_enabled: bool
    online_ping_interval_minutes: int
    last_connected_at: datetime | None = None
    proxy_id: int | None = None
    proxy_status: str | None = None
    individual_api_id: int | None = None
    individual_api_hash_masked: str | None = None
    api_id_override: int | None = None
    api_hash_override_masked: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
