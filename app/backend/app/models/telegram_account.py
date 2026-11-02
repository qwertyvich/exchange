from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AccountStatus(StrEnum):
    imported = "imported"
    active = "active"
    disabled = "disabled"
    error = "error"


class TelegramAccount(Base):
    __tablename__ = "telegram_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    phone_number: Mapped[str | None] = mapped_column(String(64), nullable=True)
    name: Mapped[str] = mapped_column(String(160), default="Imported account", nullable=False)
    username: Mapped[str | None] = mapped_column(String(160), nullable=True)
    geo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    session_file: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[AccountStatus] = mapped_column(SAEnum(AccountStatus), default=AccountStatus.imported, nullable=False)
    online_keepalive: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    online_keepalive_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    online_ping_interval_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    last_connected_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    individual_api_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    encrypted_individual_api_hash: Mapped[str | None] = mapped_column(String(512), nullable=True)
    proxy_id: Mapped[int | None] = mapped_column(ForeignKey("proxies.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    proxy = relationship("Proxy")
