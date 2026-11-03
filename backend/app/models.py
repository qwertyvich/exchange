from sqlalchemy import String, Float, Boolean, DateTime, Text, JSON, Numeric, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .db import Base

import uuid

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    give_currency_backend_id: Mapped[int] = mapped_column(nullable=False)
    give_symbol: Mapped[str] = mapped_column(String(16), nullable=False)
    give_amount: Mapped[float] = mapped_column(Numeric(36, 12), nullable=False)
    give_coingecko_id: Mapped[str] = mapped_column(String(64), nullable=False)

    get_currency_backend_id: Mapped[int] = mapped_column(nullable=False)
    get_symbol: Mapped[str] = mapped_column(String(16), nullable=False)
    get_amount: Mapped[float] = mapped_column(Numeric(36, 12), nullable=False)
    get_coingecko_id: Mapped[str] = mapped_column(String(64), nullable=True)

    get_is_fiat: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fiat_code: Mapped[str] = mapped_column(String(8), nullable=True)     # "rub"
    rub_kind: Mapped[str] = mapped_column(String(16), nullable=True)     # "sbp"/"card"/"cash"/"qr"

    fee_percent: Mapped[float] = mapped_column(Float, nullable=False)

    telegram: Mapped[str] = mapped_column(String(128), nullable=False)
    payout_details: Mapped[str] = mapped_column(String(512), nullable=False)

    give_usd: Mapped[float] = mapped_column(Float, nullable=True)
    give_rub: Mapped[float] = mapped_column(Float, nullable=True)
    get_usd: Mapped[float] = mapped_column(Float, nullable=True)

    raw_payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="new", nullable=False)
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    guest_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    quote_id: Mapped[str | None] = mapped_column(String(32), nullable=True, unique=True)

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    role: Mapped[str] = mapped_column(String(32), default="user", nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


Index("ix_tickets_user_created", Ticket.user_id, Ticket.created_at)


class SiteDocument(Base):
    __tablename__ = "site_documents"
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[dict] = mapped_column(JSON, nullable=False)


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    channel: Mapped[str] = mapped_column(String(16), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    next_attempt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[str | None] = mapped_column(String(255), nullable=True)
    attachment: Mapped[str | None] = mapped_column(String(512), nullable=True)
