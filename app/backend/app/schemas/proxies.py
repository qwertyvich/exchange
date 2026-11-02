from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ProxyTypeValue = Literal["http", "https", "socks5"]
ProxyStatusValue = Literal["unchecked", "working", "failed"]


class ProxyBase(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    type: ProxyTypeValue = "http"
    host: str = Field(min_length=1, max_length=255)
    port: int = Field(ge=1, le=65535)
    username: str | None = Field(default=None, max_length=255)
    password: str | None = None


class ProxyCreate(ProxyBase):
    pass


class ProxyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    type: ProxyTypeValue | None = None
    host: str | None = Field(default=None, min_length=1, max_length=255)
    port: int | None = Field(default=None, ge=1, le=65535)
    username: str | None = Field(default=None, max_length=255)
    password: str | None = None


class ProxyRead(BaseModel):
    id: int
    name: str
    type: str
    host: str
    port: int
    username: str | None = None
    password_masked: str | None = None
    status: str
    last_checked_at: datetime | None = None
    last_error: str | None = None

    model_config = {"from_attributes": True}
