from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

TemplateType = Literal["post", "reply", "bio", "channel_description", "generic"]


class TemplateCreate(BaseModel):
    type: TemplateType = "generic"
    title: str = Field(min_length=1, max_length=180)
    body: str = Field(min_length=1)
    locale: str | None = Field(default=None, max_length=16)


class TemplateUpdate(BaseModel):
    type: TemplateType | None = None
    title: str | None = Field(default=None, min_length=1, max_length=180)
    body: str | None = Field(default=None, min_length=1)
    locale: str | None = Field(default=None, max_length=16)


class TemplateRead(BaseModel):
    id: int
    owner_user_id: int
    type: str
    title: str
    body: str
    locale: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class TemplateRenderRead(BaseModel):
    template_id: int
    account_id: int
    rendered_body: str
