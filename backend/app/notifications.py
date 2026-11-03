"""Telegram outbox: requests commit locally; network delivery happens separately."""
import asyncio
import logging
import os
import shutil
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from aiogram import Bot
from aiogram.types import FSInputFile
from .db import SessionLocal
from .models import Notification
from .settings_loader import load_settings

log = logging.getLogger(__name__)


def enabled():
    return os.getenv("TELEGRAM_ENABLED", "false").lower() == "true"


class QueuedBot:
    # Compatibility with the existing handlers, without blocking HTTP on Telegram.
    session = None

    async def send_message(self, channel, text, **kwargs):
        if enabled():
            with SessionLocal() as db:
                db.add(Notification(channel=channel, text=text))
                db.commit()

    async def send_photo(self, channel, photo, caption="", **kwargs):
        if not enabled():
            return
        root = Path(os.getenv("UPLOAD_DIR", "/app/data/receipts"))
        root.mkdir(parents=True, exist_ok=True)
        target = root / f"{uuid.uuid4().hex}{Path(photo.path).suffix}"
        shutil.copyfile(photo.path, target)
        with SessionLocal() as db:
            db.add(Notification(channel=channel, text=caption, attachment=str(target)))
            db.commit()


async def notification_worker():
    while True:
        if enabled():
            try:
                with SessionLocal() as db:
                    item = db.query(Notification).filter(Notification.sent_at.is_(None), Notification.attempts < 8,
                        Notification.next_attempt <= datetime.utcnow()).order_by(Notification.next_attempt).with_for_update(skip_locked=True).first()
                    if item:
                        config = load_settings().get("bot", {})
                        token = os.getenv("TELEGRAM_BOT_TOKEN") or config.get("API_TOKEN")
                        chat = os.getenv("TELEGRAM_TICKETS_CHAT_ID" if item.channel == "tickets" else "TELEGRAM_MESSAGES_CHAT_ID") or config.get("CHAT_ID" if item.channel == "tickets" else "MESS_CHAT")
                        item.attempts += 1
                        try:
                            if not token or not chat:
                                raise ValueError("Telegram configuration missing")
                            async with Bot(token=token) as client:
                                if item.attachment:
                                    await client.send_document(chat, FSInputFile(item.attachment), caption=item.text, parse_mode="HTML", request_timeout=15)
                                else:
                                    await client.send_message(chat, item.text, parse_mode="HTML", request_timeout=15)
                            item.sent_at = datetime.utcnow()
                            item.last_error = None
                        except Exception as exc:
                            # Do not log the token, chat ID or customer data.
                            item.last_error = type(exc).__name__
                            item.next_attempt = datetime.utcnow() + timedelta(seconds=min(30 * 2 ** item.attempts, 3600))
                            log.warning("Telegram delivery failed (%s), retry scheduled", type(exc).__name__)
                        db.commit()
            except asyncio.CancelledError:
                raise
            except Exception:
                log.exception("Notification worker failed")
        await asyncio.sleep(2)
