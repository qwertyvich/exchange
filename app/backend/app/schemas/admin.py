from datetime import datetime

from pydantic import BaseModel


class AdminUserRead(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditLogRead(BaseModel):
    id: int
    user_id: int | None = None
    username: str | None = None
    action: str
    action_type: str
    telegram_account_id: int | None = None
    entity_type: str | None = None
    entity_id: str | None = None
    details: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
