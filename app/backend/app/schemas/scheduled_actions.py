from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


ScheduledActionStatusValue = Literal["pending", "running", "completed", "failed", "cancelled"]
ActionTypeValue = Literal[
    "change_name",
    "change_username",
    "change_bio",
    "upload_photo",
    "send_message",
    "create_channel",
    "create_group",
    "post_to_channel",
    "enable_keepalive",
    "disable_keepalive",
    "connect",
    "check_proxy",
]


class ScheduledActionCreate(BaseModel):
    telegram_account_id: int | None = None
    account_id: int | None = None
    action_type: ActionTypeValue
    payload_json: str | None = None
    scheduled_for: datetime | None = None
    run_at: datetime | None = None


class ScheduledActionUpdate(BaseModel):
    telegram_account_id: int | None = None
    account_id: int | None = None
    action_type: ActionTypeValue | None = None
    payload_json: str | None = None
    scheduled_for: datetime | None = None
    run_at: datetime | None = None
    status: ScheduledActionStatusValue | None = None


class ScheduledActionRead(BaseModel):
    id: int
    owner_user_id: int | None = None
    telegram_account_id: int | None = None
    account_id: int | None = None
    action_type: str
    payload_json: str | None = None
    scheduled_for: datetime
    run_at: datetime
    status: str
    result_json: str | None = None
    error: str | None = None
    created_by_user_id: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
