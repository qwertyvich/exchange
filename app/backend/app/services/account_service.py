from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.proxy import ProxyStatus
from app.models.scheduled_action import ScheduledAction, ScheduledActionStatus
from app.models.telegram_account import AccountStatus, TelegramAccount
from app.models.user import User
from app.schemas.accounts import AccountCreate, AccountUpdate
from app.services.audit_service import write_audit_log
from app.storage.secrets import SecretStorage
from app.storage.sessions import delete_session_file, save_session_file


def serialize_account(account: TelegramAccount) -> dict:
    masked_hash = SecretStorage.mask(account.encrypted_individual_api_hash)
    return {
        "id": account.id,
        "phone_number": account.phone_number,
        "name": account.name,
        "display_name": account.name,
        "username": account.username,
        "geo": account.geo,
        "session_file": account.session_file,
        "status": account.status.value,
        "online_keepalive": account.online_keepalive_enabled,
        "online_keepalive_enabled": account.online_keepalive_enabled,
        "online_ping_interval_minutes": account.online_ping_interval_minutes,
        "last_connected_at": account.last_connected_at,
        "proxy_id": account.proxy_id,
        "proxy_status": account.proxy.status.value if account.proxy else None,
        "individual_api_id": account.individual_api_id,
        "individual_api_hash_masked": masked_hash,
        "api_id_override": account.individual_api_id,
        "api_hash_override_masked": masked_hash,
        "created_at": account.created_at,
    }


def create_account(db: Session, payload: AccountCreate, user: User) -> TelegramAccount:
    data = payload.model_dump(exclude={"api_hash_override", "api_id_override", "individual_api_hash", "display_name"})
    data["name"] = payload.display_name or payload.name
    data["session_file"] = data.get("session_file") or ""
    data["online_keepalive"] = payload.online_keepalive_enabled or payload.online_keepalive
    data["individual_api_id"] = payload.individual_api_id or payload.api_id_override
    individual_hash = payload.individual_api_hash or payload.api_hash_override
    if individual_hash is not None:
        data["encrypted_individual_api_hash"] = SecretStorage.store(individual_hash)
    account = TelegramAccount(**data)
    db.add(account)
    db.commit()
    db.refresh(account)
    write_audit_log(db, user, "account.create", "TelegramAccount", str(account.id))
    return account


def import_session(
    db: Session,
    file: UploadFile,
    user: User,
    phone_number: str | None = None,
    geo: str | None = None,
    proxy_id: int | None = None,
    api_id_override: int | None = None,
    api_hash_override: str | None = None,
) -> TelegramAccount:
    session_file = save_session_file(file)
    account = TelegramAccount(
        name=file.filename or "Imported account",
        session_file=session_file,
        phone_number=phone_number,
        geo=geo,
        proxy_id=proxy_id,
        individual_api_id=api_id_override,
        encrypted_individual_api_hash=SecretStorage.store(api_hash_override),
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    details = "Session file imported"
    if account.proxy and account.proxy.status != ProxyStatus.working:
        details += "; proxy is not working, automatic connection skipped"
    write_audit_log(db, user, "account.import_session", "TelegramAccount", str(account.id), details)
    return account


def update_account(db: Session, account: TelegramAccount, payload: AccountUpdate, user: User) -> TelegramAccount:
    data = payload.model_dump(exclude_unset=True)
    api_hash = data.pop("individual_api_hash", None)
    legacy_api_hash = data.pop("api_hash_override", None)
    if api_hash is None:
        api_hash = legacy_api_hash
    legacy_api_id = data.pop("api_id_override", None)
    if legacy_api_id is not None and "individual_api_id" not in data:
        data["individual_api_id"] = legacy_api_id
    display_name = data.pop("display_name", None)
    if display_name is not None:
        data["name"] = display_name
    for key, value in data.items():
        if hasattr(account, key):
            if key == "status" and value is not None:
                value = AccountStatus(value)
            setattr(account, key, value)
            if key == "online_keepalive_enabled":
                account.online_keepalive = bool(value)
            if key == "online_keepalive":
                account.online_keepalive_enabled = bool(value)
    if api_hash is not None:
        account.encrypted_individual_api_hash = SecretStorage.store(api_hash)
    db.commit()
    db.refresh(account)
    write_audit_log(db, user, "account.update", "TelegramAccount", str(account.id))
    return account


def update_account_credentials(
    db: Session,
    account: TelegramAccount,
    user: User,
    individual_api_id: int | None,
    individual_api_hash: str | None,
) -> TelegramAccount:
    account.individual_api_id = individual_api_id
    if individual_api_hash is not None:
        account.encrypted_individual_api_hash = SecretStorage.store(individual_api_hash)
    db.commit()
    db.refresh(account)
    write_audit_log(
        db,
        user,
        "account.credentials.update",
        "TelegramAccount",
        str(account.id),
        "Individual API credentials updated",
    )
    return account


def delete_account(db: Session, account: TelegramAccount, user: User) -> None:
    db.query(ScheduledAction).filter(
        ScheduledAction.telegram_account_id == account.id,
        ScheduledAction.status == ScheduledActionStatus.pending,
    ).update({"status": ScheduledActionStatus.cancelled}, synchronize_session=False)
    session_deleted = delete_session_file(account.session_file)
    account_id = account.id
    db.delete(account)
    db.commit()
    details = "Account deleted"
    if session_deleted:
        details += "; session file deleted"
    write_audit_log(db, user, "account.delete", "TelegramAccount", str(account_id), details)
