from datetime import datetime
import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.telegram_account import TelegramAccount
from app.models.template import Template
from app.models.user import User
from app.schemas.templates import TemplateCreate, TemplateUpdate
from app.services.audit_service import write_audit_log

ALLOWED_TEMPLATE_VARIABLES = {
    "first_name",
    "last_name",
    "username",
    "phone_number",
    "date",
}
VARIABLE_PATTERN = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")


def create_template(db: Session, payload: TemplateCreate, user: User) -> Template:
    data = payload.model_dump()
    template = Template(**data, content=data["body"], owner_user_id=user.id)
    db.add(template)
    db.commit()
    db.refresh(template)
    write_audit_log(db, user, "template.create", "Template", str(template.id))
    return template


def update_template(db: Session, template: Template, payload: TemplateUpdate, user: User) -> Template:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(template, key, value)
        if key == "body":
            template.content = value
    db.commit()
    db.refresh(template)
    write_audit_log(db, user, "template.update", "Template", str(template.id))
    return template


def render_template(template: Template, account: TelegramAccount) -> str:
    display_name = account.name or ""
    name_parts = display_name.split(maxsplit=1)
    values = {
        "first_name": name_parts[0] if name_parts else "",
        "last_name": name_parts[1] if len(name_parts) > 1 else "",
        "username": account.username or "",
        "phone_number": account.phone_number or "",
        "date": datetime.utcnow().date().isoformat(),
    }

    def replace(match: re.Match[str]) -> str:
        variable = match.group(1)
        if variable not in ALLOWED_TEMPLATE_VARIABLES:
            raise HTTPException(status_code=400, detail=f"Unsupported template variable: {variable}")
        return values[variable]

    return VARIABLE_PATTERN.sub(replace, template.body)
