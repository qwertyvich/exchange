from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AppSettings(Base):
    __tablename__ = "app_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    global_api_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    encrypted_global_api_hash: Mapped[str | None] = mapped_column(String(512), nullable=True)
    default_online_ping_minutes: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    message_rate_limit_per_minute: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
