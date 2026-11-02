from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.scheduled_action import ActionType, ScheduledAction, ScheduledActionStatus
from app.models.telegram_account import TelegramAccount
from app.models.user import User, UserRole
from app.services.audit_service import write_audit_log
from app.services.proxy_service import check_proxy
from app.services.telegram_service import TelethonService

Handler = Callable[[ScheduledAction, Session], dict]

scheduler = BackgroundScheduler(timezone="UTC")


def _utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _as_utc_naive(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _parse_payload(action: ScheduledAction) -> dict:
    if not action.payload_json:
        return {}
    try:
        return json.loads(action.payload_json)
    except json.JSONDecodeError:
        return {}


def _stub_result(action: ScheduledAction, db: Session) -> dict:
    return {
        "status": "stub",
        "action_type": action.action_type,
        "message": "Telegram action handler is prepared for MVP; real Telethon execution is TODO.",
    }


def _account_or_error(action: ScheduledAction, db: Session) -> TelegramAccount:
    if action.telegram_account_id is None:
        raise ValueError("telegram_account_id is required")
    account = db.get(TelegramAccount, action.telegram_account_id)
    if not account:
        raise ValueError("Telegram account not found")
    return account


def _change_name(action: ScheduledAction, db: Session) -> dict:
    payload = _parse_payload(action)
    return TelethonService().change_name(_account_or_error(action, db), payload.get("first_name", ""), payload.get("last_name"))


def _change_username(action: ScheduledAction, db: Session) -> dict:
    payload = _parse_payload(action)
    return TelethonService().change_username(_account_or_error(action, db), payload.get("username", ""))


def _change_bio(action: ScheduledAction, db: Session) -> dict:
    payload = _parse_payload(action)
    return TelethonService().change_bio(_account_or_error(action, db), payload.get("bio", ""))


def _upload_photo(action: ScheduledAction, db: Session) -> dict:
    payload = _parse_payload(action)
    return TelethonService().upload_profile_photo(_account_or_error(action, db), file_path=payload.get("file_path"))


def _connect(action: ScheduledAction, db: Session) -> dict:
    return TelethonService().connect_account(_account_or_error(action, db))


def _check_proxy(action: ScheduledAction, db: Session) -> dict:
    account = _account_or_error(action, db)
    if not account.proxy:
        raise ValueError("Account has no proxy")
    proxy = check_proxy(db, account.proxy, None)
    return {"proxy_id": proxy.id, "status": proxy.status.value, "last_error": proxy.last_error}


def _set_keepalive(action: ScheduledAction, db: Session, enabled: bool) -> dict:
    if action.telegram_account_id is None:
        raise ValueError("telegram_account_id is required for keepalive actions")
    account = db.get(TelegramAccount, action.telegram_account_id)
    if not account:
        raise ValueError("Telegram account not found")
    account.online_keepalive_enabled = enabled
    account.online_keepalive = enabled
    db.flush()
    return {"online_keepalive": enabled}


def _enable_keepalive(action: ScheduledAction, db: Session) -> dict:
    return _set_keepalive(action, db, True)


def _disable_keepalive(action: ScheduledAction, db: Session) -> dict:
    return _set_keepalive(action, db, False)


ACTION_HANDLERS: dict[str, Handler] = {
    ActionType.change_name.value: _change_name,
    ActionType.change_username.value: _change_username,
    ActionType.change_bio.value: _change_bio,
    ActionType.upload_photo.value: _upload_photo,
    ActionType.send_message.value: _stub_result,
    ActionType.create_channel.value: _stub_result,
    ActionType.create_group.value: _stub_result,
    ActionType.post_to_channel.value: _stub_result,
    ActionType.enable_keepalive.value: _enable_keepalive,
    ActionType.disable_keepalive.value: _disable_keepalive,
    ActionType.connect.value: _connect,
    ActionType.check_proxy.value: _check_proxy,
}


def schedule_pending_actions() -> None:
    with SessionLocal() as db:
        actions = db.query(ScheduledAction).filter(ScheduledAction.status == ScheduledActionStatus.pending).all()
        for action in actions:
            add_scheduler_job(action)


def start_scheduler() -> None:
    if not scheduler.running:
        scheduler.start()
    schedule_pending_actions()
    scheduler.add_job(
        run_keepalive_tick,
        trigger="interval",
        minutes=15,
        id="keepalive-tick",
        replace_existing=True,
        max_instances=1,
    )


def shutdown_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)


def add_scheduler_job(action: ScheduledAction) -> None:
    if action.status != ScheduledActionStatus.pending:
        return
    run_date = action.scheduled_for
    if run_date <= _utc_now_naive():
        run_date = _utc_now_naive()
    scheduler.add_job(
        execute_action_by_id,
        trigger="date",
        run_date=run_date,
        args=[action.id],
        id=f"scheduled-action-{action.id}",
        replace_existing=True,
        misfire_grace_time=3600,
    )


def execute_action_by_id(action_id: int) -> None:
    with SessionLocal() as db:
        action = db.get(ScheduledAction, action_id)
        if not action or action.status != ScheduledActionStatus.pending:
            return
        execute_action(db, action)


def execute_action(db: Session, action: ScheduledAction) -> ScheduledAction:
    handler = ACTION_HANDLERS.get(action.action_type)
    if not handler:
        action.status = ScheduledActionStatus.failed
        action.error = f"Unsupported action_type: {action.action_type}"
        db.commit()
        db.refresh(action)
        write_audit_log(db, None, "scheduled_action.failed", "ScheduledAction", str(action.id), action.error)
        return action

    action.status = ScheduledActionStatus.running
    action.error = None
    db.commit()
    db.refresh(action)
    write_audit_log(db, None, "scheduled_action.running", "ScheduledAction", str(action.id))

    try:
        result = handler(action, db)
        action.result_json = json.dumps(result, ensure_ascii=False)
        action.status = ScheduledActionStatus.completed
        action.error = None
        db.commit()
        db.refresh(action)
        write_audit_log(db, None, "scheduled_action.completed", "ScheduledAction", str(action.id))
    except Exception as exc:
        action.status = ScheduledActionStatus.failed
        action.error = f"{exc.__class__.__name__}: {exc}"
        db.commit()
        db.refresh(action)
        write_audit_log(db, None, "scheduled_action.failed", "ScheduledAction", str(action.id), action.error)
    return action


def run_keepalive_tick() -> None:
    with SessionLocal() as db:
        now = _utc_now_naive()
        accounts = db.query(TelegramAccount).filter(TelegramAccount.online_keepalive_enabled.is_(True)).all()
        service = TelethonService()
        for account in accounts:
            interval = max(15, account.online_ping_interval_minutes or 15)
            if account.last_connected_at and account.last_connected_at > now - timedelta(minutes=interval):
                continue
            try:
                result = service.keepalive_ping(account)
                db.commit()
                write_audit_log(
                    db,
                    None,
                    "account.keepalive_ping",
                    "TelegramAccount",
                    str(account.id),
                    json.dumps({"status": result.get("status")}),
                )
            except Exception as exc:
                db.rollback()
                write_audit_log(
                    db,
                    None,
                    "account.keepalive_ping.failed",
                    "TelegramAccount",
                    str(account.id),
                    f"{exc.__class__.__name__}: {exc}",
                )


def cancel_action(db: Session, action: ScheduledAction, user: User | None = None) -> ScheduledAction:
    if user and user.role != UserRole.admin and action.owner_user_id != user.id:
        raise HTTPException(status_code=403, detail="Only owner or Admin can cancel this action")
    if action.status != ScheduledActionStatus.pending:
        raise HTTPException(status_code=409, detail="Only pending actions can be cancelled")
    action.status = ScheduledActionStatus.cancelled
    db.commit()
    db.refresh(action)
    try:
        scheduler.remove_job(f"scheduled-action-{action.id}")
    except Exception:
        pass
    write_audit_log(db, user, "scheduled_action.cancel", "ScheduledAction", str(action.id))
    return action


def create_scheduled_action(
    db: Session,
    owner_user_id: int | None,
    action_type: str,
    payload_json: str | None,
    telegram_account_id: int | None,
    scheduled_for: datetime | None,
) -> ScheduledAction:
    action = ScheduledAction(
        owner_user_id=owner_user_id,
        created_by_user_id=owner_user_id,
        telegram_account_id=telegram_account_id,
        account_id=telegram_account_id,
        action_type=action_type,
        payload_json=payload_json,
        scheduled_for=_as_utc_naive(scheduled_for) or _utc_now_naive(),
        run_at=_as_utc_naive(scheduled_for) or _utc_now_naive(),
        status=ScheduledActionStatus.pending,
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return action


def execute_now_or_schedule(
    db: Session,
    owner_user_id: int | None,
    action_type: str,
    payload_json: str | None = None,
    account_id: int | None = None,
    schedule_for: datetime | None = None,
) -> ScheduledAction:
    action = create_scheduled_action(db, owner_user_id, action_type, payload_json, account_id, schedule_for)
    if schedule_for is None:
        execute_action(db, action)
    else:
        add_scheduler_job(action)
    return action
