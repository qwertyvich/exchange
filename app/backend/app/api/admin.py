from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.scheduled_actions import get_action_or_404
from app.core.database import get_db
from app.core.security import require_admin
from app.models.audit_log import AuditLog
from app.models.scheduled_action import ScheduledAction
from app.models.user import User
from app.schemas.admin import AdminUserRead, AuditLogRead
from app.schemas.scheduled_actions import ScheduledActionRead
from app.services.scheduler_service import cancel_action

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[AdminUserRead])
def list_users(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> list[User]:
    return db.query(User).order_by(User.id.asc()).offset(offset).limit(limit).all()


@router.get("/audit-logs", response_model=list[AuditLogRead])
def list_audit_logs(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    user_id: int | None = Query(default=None),
    telegram_account_id: int | None = Query(default=None),
    action_type: str | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> list[AuditLog]:
    query = db.query(AuditLog)
    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)
    if telegram_account_id is not None:
        query = query.filter(AuditLog.entity_type == "TelegramAccount", AuditLog.entity_id == str(telegram_account_id))
    if action_type:
        query = query.filter(AuditLog.action == action_type)
    if date_from:
        query = query.filter(AuditLog.created_at >= date_from)
    if date_to:
        query = query.filter(AuditLog.created_at <= date_to)
    return query.order_by(AuditLog.id.desc()).offset(offset).limit(limit).all()


@router.get("/scheduled-actions", response_model=list[ScheduledActionRead])
def admin_scheduled_actions(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    status: str | None = Query(default=None),
    account_id: int | None = Query(default=None),
    action_type: str | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> list[ScheduledAction]:
    query = db.query(ScheduledAction)
    if status:
        query = query.filter(ScheduledAction.status == status)
    if account_id is not None:
        query = query.filter(ScheduledAction.telegram_account_id == account_id)
    if action_type:
        query = query.filter(ScheduledAction.action_type == action_type)
    if date_from:
        query = query.filter(ScheduledAction.scheduled_for >= date_from)
    if date_to:
        query = query.filter(ScheduledAction.scheduled_for <= date_to)
    return query.order_by(ScheduledAction.id.desc()).offset(offset).limit(limit).all()


@router.post("/scheduled-actions/{action_id}/cancel", response_model=ScheduledActionRead)
def admin_cancel_action(action_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)) -> ScheduledAction:
    return cancel_action(db, get_action_or_404(db, action_id), current_user)
