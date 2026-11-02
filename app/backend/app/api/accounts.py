from pathlib import Path
from uuid import uuid4
import json
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.proxy import Proxy
from app.models.app_settings import AppSettings
from app.models.audit_log import AuditLog
from app.models.telegram_account import TelegramAccount
from app.models.user import User
from app.models.scheduled_action import ActionType
from app.schemas.accounts import AccountCreate, AccountCredentialsUpdate, AccountRead, AccountUpdate
from app.schemas.accounts import ChangeBioPayload, ChangeNamePayload, ChangeUsernamePayload, KeepaliveUpdate, ScheduledPayload
from app.schemas.accounts import SendDialogMessagePayload, SendUsernameMessagePayload
from app.schemas.scheduled_actions import ScheduledActionRead
from app.services.account_service import create_account, delete_account as delete_account_service
from app.services.account_service import import_session, serialize_account, update_account, update_account_credentials
from app.services.audit_service import write_audit_log
from app.services.proxy_service import check_proxy
from app.services.scheduler_service import execute_now_or_schedule
from app.services.telegram_service import TelethonService

UPLOADS_DIR = Path(__file__).resolve().parents[2] / "data" / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/accounts", tags=["accounts"])


def get_account_or_404(db: Session, account_id: int) -> TelegramAccount:
    account = db.get(TelegramAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


def _message_rate_limit(db: Session, account: TelegramAccount) -> None:
    settings = db.query(AppSettings).first()
    limit = settings.message_rate_limit_per_minute if settings else 5
    since = datetime.utcnow() - timedelta(minutes=1)
    sent_count = (
        db.query(AuditLog)
        .filter(
            AuditLog.entity_type == "TelegramAccount",
            AuditLog.entity_id == str(account.id),
            AuditLog.action.in_(["message.send_dialog", "message.send_username"]),
            AuditLog.created_at >= since,
        )
        .count()
    )
    if sent_count >= limit:
        raise HTTPException(status_code=429, detail=f"Message rate limit exceeded: {limit} messages per minute")


@router.get("", response_model=list[AccountRead])
def list_accounts(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    search: str | None = Query(default=None),
    status: str | None = Query(default=None),
    geo: str | None = Query(default=None),
    proxy_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[dict]:
    query = db.query(TelegramAccount)
    if search:
        needle = f"%{search}%"
        query = query.filter(
            or_(
                TelegramAccount.phone_number.ilike(needle),
                TelegramAccount.name.ilike(needle),
                TelegramAccount.username.ilike(needle),
            )
        )
    if status:
        query = query.filter(TelegramAccount.status == status)
    if geo:
        query = query.filter(TelegramAccount.geo == geo)
    if proxy_id is not None:
        query = query.filter(TelegramAccount.proxy_id == proxy_id)
    accounts = query.order_by(TelegramAccount.id.desc()).offset(offset).limit(limit).all()
    return [serialize_account(account) for account in accounts]


@router.post("", response_model=AccountRead)
def create_account_endpoint(payload: AccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    if payload.proxy_id is not None and not db.get(Proxy, payload.proxy_id):
        raise HTTPException(status_code=404, detail="Proxy not found")
    return serialize_account(create_account(db, payload, current_user))


@router.post("/import-session", response_model=AccountRead)
def upload_session(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    try:
        account = import_session(db, file, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return serialize_account(account)


@router.post("/import-session-with-meta", response_model=AccountRead)
def upload_session_with_meta(
    file: UploadFile = File(...),
    phone_number: str | None = Form(default=None),
    geo: str | None = Form(default=None),
    proxy_id: int | None = Form(default=None),
    api_id_override: int | None = Form(default=None),
    api_hash_override: str | None = Form(default=None),
    individual_api_id: int | None = Form(default=None),
    individual_api_hash: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    if proxy_id is not None and not db.get(Proxy, proxy_id):
        raise HTTPException(status_code=404, detail="Proxy not found")
    try:
        account = import_session(
            db,
            file,
            current_user,
            phone_number=phone_number,
            geo=geo,
            proxy_id=proxy_id,
            api_id_override=individual_api_id or api_id_override,
            api_hash_override=individual_api_hash or api_hash_override,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return serialize_account(account)


@router.get("/{account_id}", response_model=AccountRead)
def read_account(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return serialize_account(get_account_or_404(db, account_id))


@router.get("/{account_id}/dialogs")
def list_account_dialogs(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[dict]:
    account = get_account_or_404(db, account_id)
    dialogs = TelethonService().list_dialogs(account)
    write_audit_log(db, current_user, "dialogs.list", "TelegramAccount", str(account.id))
    return dialogs


@router.get("/{account_id}/dialogs/{dialog_id}/messages")
def list_dialog_messages(
    account_id: int,
    dialog_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[dict]:
    account = get_account_or_404(db, account_id)
    messages = TelethonService().list_messages(account, dialog_id, limit, offset)
    write_audit_log(db, current_user, "messages.list", "TelegramAccount", str(account.id), f"dialog_id={dialog_id}")
    return messages


@router.post("/{account_id}/dialogs/{dialog_id}/send-message")
def send_dialog_message(
    account_id: int,
    dialog_id: str,
    payload: SendDialogMessagePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    account = get_account_or_404(db, account_id)
    _message_rate_limit(db, account)
    result = TelethonService().send_message_to_existing_dialog(account, dialog_id, payload.text)
    write_audit_log(db, current_user, "message.send_dialog", "TelegramAccount", str(account.id), f"dialog_id={dialog_id}")
    return result


@router.post("/{account_id}/send-message-by-username")
def send_message_by_username(
    account_id: int,
    payload: SendUsernameMessagePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    account = get_account_or_404(db, account_id)
    if not payload.confirmed:
        raise HTTPException(status_code=400, detail="Sending by username requires confirmed=true")
    _message_rate_limit(db, account)
    result = TelethonService().send_message_by_username(account, payload.username, payload.text, payload.confirmed)
    write_audit_log(db, current_user, "message.send_username", "TelegramAccount", str(account.id), f"username={payload.username}")
    return result


@router.put("/{account_id}", response_model=AccountRead)
def update_account_endpoint(account_id: int, payload: AccountUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    if payload.proxy_id is not None and not db.get(Proxy, payload.proxy_id):
        raise HTTPException(status_code=404, detail="Proxy not found")
    return serialize_account(update_account(db, get_account_or_404(db, account_id), payload, current_user))


@router.put("/{account_id}/credentials", response_model=AccountRead)
def update_account_credentials_endpoint(
    account_id: int,
    payload: AccountCredentialsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    account = get_account_or_404(db, account_id)
    updated = update_account_credentials(
        db,
        account,
        current_user,
        individual_api_id=payload.individual_api_id,
        individual_api_hash=payload.individual_api_hash,
    )
    return serialize_account(updated)


def _execute_account_action(
    db: Session,
    user: User,
    account: TelegramAccount,
    action_type: str,
    payload: dict,
    schedule_for,
):
    action = execute_now_or_schedule(
        db,
        owner_user_id=user.id,
        action_type=action_type,
        payload_json=json.dumps(payload, ensure_ascii=False),
        account_id=account.id,
        schedule_for=schedule_for,
    )
    write_audit_log(db, user, f"account.action.{action_type}", "TelegramAccount", str(account.id), "Account action requested")
    return action


@router.post("/{account_id}/actions/change-name", response_model=ScheduledActionRead)
def change_name_action(
    account_id: int,
    payload: ChangeNamePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_account_or_404(db, account_id)
    return _execute_account_action(
        db,
        current_user,
        account,
        ActionType.change_name.value,
        {"first_name": payload.first_name, "last_name": payload.last_name},
        payload.schedule_for,
    )


@router.post("/{account_id}/actions/change-username", response_model=ScheduledActionRead)
def change_username_action(
    account_id: int,
    payload: ChangeUsernamePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_account_or_404(db, account_id)
    return _execute_account_action(
        db,
        current_user,
        account,
        ActionType.change_username.value,
        {"username": payload.username},
        payload.schedule_for,
    )


@router.post("/{account_id}/actions/change-bio", response_model=ScheduledActionRead)
def change_bio_action(
    account_id: int,
    payload: ChangeBioPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_account_or_404(db, account_id)
    return _execute_account_action(db, current_user, account, ActionType.change_bio.value, {"bio": payload.bio}, payload.schedule_for)


@router.post("/{account_id}/actions/upload-photo", response_model=ScheduledActionRead)
def upload_photo_action(
    account_id: int,
    file: UploadFile = File(...),
    schedule_for: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from datetime import datetime

    account = get_account_or_404(db, account_id)
    safe_name = f"{uuid4().hex}_{Path(file.filename or 'profile-photo').name}"
    target = UPLOADS_DIR / safe_name
    with target.open("wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            buffer.write(chunk)
    scheduled_for = datetime.fromisoformat(schedule_for.replace("Z", "+00:00")) if schedule_for else None
    return _execute_account_action(
        db,
        current_user,
        account,
        ActionType.upload_photo.value,
        {"file_path": safe_name, "file_name": file.filename},
        scheduled_for,
    )


@router.put("/{account_id}/keepalive", response_model=AccountRead)
def update_keepalive(
    account_id: int,
    payload: KeepaliveUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    account = get_account_or_404(db, account_id)
    account.online_keepalive_enabled = payload.online_keepalive_enabled
    account.online_keepalive = payload.online_keepalive_enabled
    account.online_ping_interval_minutes = payload.online_ping_interval_minutes
    db.commit()
    db.refresh(account)
    write_audit_log(db, current_user, "account.keepalive.update", "TelegramAccount", str(account.id))
    return serialize_account(account)


@router.post("/{account_id}/connect", response_model=ScheduledActionRead)
def connect_account_action(
    account_id: int,
    payload: ScheduledPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_account_or_404(db, account_id)
    return _execute_account_action(db, current_user, account, ActionType.connect.value, {}, payload.schedule_for)


@router.post("/{account_id}/check-proxy")
def check_account_proxy(
    account_id: int,
    payload: ScheduledPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_account_or_404(db, account_id)
    if payload.schedule_for:
        return _execute_account_action(db, current_user, account, ActionType.check_proxy.value, {}, payload.schedule_for)
    if not account.proxy:
        raise HTTPException(status_code=404, detail="Account has no proxy")
    proxy = check_proxy(db, account.proxy, current_user)
    write_audit_log(db, current_user, "account.proxy.check", "TelegramAccount", str(account.id), f"proxy_status={proxy.status.value}")
    return {"proxy_id": proxy.id, "status": proxy.status.value, "last_error": proxy.last_error}


@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    account = get_account_or_404(db, account_id)
    delete_account_service(db, account, current_user)
    return {"ok": True}
