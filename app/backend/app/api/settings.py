from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.app_settings import AppSettings
from app.models.user import User
from app.schemas.settings import SettingsRead, SettingsUpdate
from app.services.audit_service import write_audit_log
from app.storage.secrets import SecretStorage

router = APIRouter(prefix="/settings", tags=["settings"])


def get_or_create_settings(db: Session) -> AppSettings:
    settings = db.query(AppSettings).first()
    if not settings:
        settings = AppSettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.get("", response_model=SettingsRead)
def read_settings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> SettingsRead:
    settings = get_or_create_settings(db)
    return SettingsRead(
        global_api_id=settings.global_api_id,
        global_api_hash_masked=SecretStorage.mask(settings.encrypted_global_api_hash),
        default_online_ping_minutes=settings.default_online_ping_minutes,
        default_online_ping_interval=settings.default_online_ping_minutes * 60,
        message_rate_limit_per_minute=settings.message_rate_limit_per_minute,
    )


@router.put("", response_model=SettingsRead)
def update_settings(payload: SettingsUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> SettingsRead:
    settings = get_or_create_settings(db)
    settings.global_api_id = payload.global_api_id
    if payload.global_api_hash is not None:
        settings.encrypted_global_api_hash = SecretStorage.store(payload.global_api_hash)
    if payload.default_online_ping_minutes is not None:
        settings.default_online_ping_minutes = payload.default_online_ping_minutes
    elif payload.default_online_ping_interval is not None:
        settings.default_online_ping_minutes = max(1, payload.default_online_ping_interval // 60)
    if payload.message_rate_limit_per_minute is not None:
        settings.message_rate_limit_per_minute = payload.message_rate_limit_per_minute
    db.commit()
    db.refresh(settings)
    write_audit_log(db, current_user, "settings.update", "AppSettings", str(settings.id))
    return SettingsRead(
        global_api_id=settings.global_api_id,
        global_api_hash_masked=SecretStorage.mask(settings.encrypted_global_api_hash),
        default_online_ping_minutes=settings.default_online_ping_minutes,
        default_online_ping_interval=settings.default_online_ping_minutes * 60,
        message_rate_limit_per_minute=settings.message_rate_limit_per_minute,
    )
