from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.scheduled_action import ScheduledAction, ScheduledActionStatus
from app.models.telegram_account import TelegramAccount
from app.models.user import User
from app.schemas.scheduled_actions import ScheduledActionCreate, ScheduledActionRead
from app.services.audit_service import write_audit_log
from app.services.scheduler_service import add_scheduler_job, cancel_action, execute_now_or_schedule

router = APIRouter(prefix="/scheduled-actions", tags=["scheduled-actions"])


def get_action_or_404(db: Session, action_id: int) -> ScheduledAction:
    action = db.get(ScheduledAction, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Scheduled action not found")
    return action


@router.get("", response_model=list[ScheduledActionRead])
def list_scheduled_actions(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    status: str | None = Query(default=None),
    account_id: int | None = Query(default=None),
    telegram_account_id: int | None = Query(default=None),
    action_type: str | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ScheduledAction]:
    query = db.query(ScheduledAction)
    if status:
        query = query.filter(ScheduledAction.status == status)
    account_filter = telegram_account_id if telegram_account_id is not None else account_id
    if account_filter is not None:
        query = query.filter(ScheduledAction.telegram_account_id == account_filter)
    if action_type:
        query = query.filter(ScheduledAction.action_type == action_type)
    if date_from:
        query = query.filter(ScheduledAction.scheduled_for >= date_from)
    if date_to:
        query = query.filter(ScheduledAction.scheduled_for <= date_to)
    return query.order_by(ScheduledAction.id.desc()).offset(offset).limit(limit).all()


@router.post("", response_model=ScheduledActionRead)
def create_scheduled_action(
    payload: ScheduledActionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScheduledAction:
    account_id = payload.telegram_account_id if payload.telegram_account_id is not None else payload.account_id
    if account_id is not None and not db.get(TelegramAccount, account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    scheduled_for = payload.scheduled_for if payload.scheduled_for is not None else payload.run_at
    action = execute_now_or_schedule(
        db,
        owner_user_id=current_user.id,
        action_type=payload.action_type,
        payload_json=payload.payload_json,
        account_id=account_id,
        schedule_for=scheduled_for,
    )
    write_audit_log(db, current_user, "scheduled_action.create", "ScheduledAction", str(action.id))
    return action


@router.get("/{action_id}", response_model=ScheduledActionRead)
def read_scheduled_action(
    action_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScheduledAction:
    return get_action_or_404(db, action_id)


@router.post("/{action_id}/cancel", response_model=ScheduledActionRead)
def cancel_scheduled_action(
    action_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScheduledAction:
    return cancel_action(db, get_action_or_404(db, action_id), current_user)


@router.delete("/{action_id}")
def delete_scheduled_action(
    action_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    action = get_action_or_404(db, action_id)
    if action.status == ScheduledActionStatus.pending:
        cancel_action(db, action, current_user)
    db.delete(action)
    db.commit()
    write_audit_log(db, current_user, "scheduled_action.delete", "ScheduledAction", str(action_id))
    return {"ok": True}
