from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.telegram_account import TelegramAccount
from app.models.template import Template
from app.models.user import User, UserRole
from app.schemas.templates import TemplateCreate, TemplateRead, TemplateRenderRead, TemplateType, TemplateUpdate
from app.services.audit_service import write_audit_log
from app.services.template_service import create_template, render_template, update_template

router = APIRouter(prefix="/templates", tags=["templates"])


def get_template_or_404(db: Session, template_id: int, current_user: User) -> Template:
    template = db.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if current_user.role != UserRole.admin and template.owner_user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.get("", response_model=list[TemplateRead])
def list_templates(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    type: TemplateType | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Template]:
    query = db.query(Template)
    if current_user.role != UserRole.admin:
        query = query.filter(Template.owner_user_id == current_user.id)
    if type:
        query = query.filter(Template.type == type)
    if search:
        needle = f"%{search}%"
        query = query.filter(or_(Template.title.ilike(needle), Template.body.ilike(needle)))
    return query.order_by(Template.id.desc()).offset(offset).limit(limit).all()


@router.post("", response_model=TemplateRead)
def create_template_endpoint(payload: TemplateCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Template:
    return create_template(db, payload, current_user)


@router.get("/{template_id}", response_model=TemplateRead)
def read_template(template_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Template:
    return get_template_or_404(db, template_id, current_user)


@router.get("/{template_id}/render", response_model=TemplateRenderRead)
def render_template_endpoint(
    template_id: int,
    account_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    template = get_template_or_404(db, template_id, current_user)
    account = db.get(TelegramAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"template_id": template.id, "account_id": account.id, "rendered_body": render_template(template, account)}


@router.put("/{template_id}", response_model=TemplateRead)
def update_template_endpoint(template_id: int, payload: TemplateUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Template:
    return update_template(db, get_template_or_404(db, template_id, current_user), payload, current_user)


@router.delete("/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    template = get_template_or_404(db, template_id, current_user)
    db.delete(template)
    db.commit()
    write_audit_log(db, current_user, "template.delete", "Template", str(template_id))
    return {"ok": True}
