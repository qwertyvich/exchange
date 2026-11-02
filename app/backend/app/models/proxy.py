from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProxyType(StrEnum):
    http = "http"
    https = "https"
    socks5 = "socks5"


class ProxyStatus(StrEnum):
    unchecked = "unchecked"
    working = "working"
    failed = "failed"


class Proxy(Base):
    __tablename__ = "proxies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    type: Mapped[ProxyType] = mapped_column(Enum(ProxyType), default=ProxyType.http, nullable=False)
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    encrypted_password: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[ProxyStatus] = mapped_column(Enum(ProxyStatus), default=ProxyStatus.unchecked, nullable=False)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
