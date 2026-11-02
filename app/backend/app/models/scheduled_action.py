from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ScheduledActionStatus(StrEnum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class ActionType(StrEnum):
    change_name = "change_name"
    change_username = "change_username"
    change_bio = "change_bio"
    upload_photo = "upload_photo"
    send_message = "send_message"
    create_channel = "create_channel"
    create_group = "create_group"
    post_to_channel = "post_to_channel"
    enable_keepalive = "enable_keepalive"
    disable_keepalive = "disable_keepalive"
    connect = "connect"
    check_proxy = "check_proxy"


class ScheduledAction(Base):
    __tablename__ = "scheduled_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    telegram_account_id: Mapped[int | None] = mapped_column(ForeignKey("telegram_accounts.id"), nullable=True)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    account_id: Mapped[int | None] = mapped_column(ForeignKey("telegram_accounts.id"), nullable=True)
    action_type: Mapped[str] = mapped_column(String(120), nullable=False)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    run_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[ScheduledActionStatus] = mapped_column(SAEnum(ScheduledActionStatus), default=ScheduledActionStatus.pending, nullable=False)
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
