from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.proxy import Proxy
from app.models.telegram_account import TelegramAccount
from app.models.user import User
from app.schemas.proxies import ProxyCreate, ProxyRead, ProxyUpdate
from app.services.audit_service import write_audit_log
from app.services.proxy_service import check_proxy, create_proxy, serialize_proxy, update_proxy

router = APIRouter(prefix="/proxies", tags=["proxies"])


def get_proxy_or_404(db: Session, proxy_id: int) -> Proxy:
    proxy = db.get(Proxy, proxy_id)
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy not found")
    return proxy


@router.get("", response_model=list[ProxyRead])
def list_proxies(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    status: str | None = Query(default=None),
    type: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[dict]:
    query = db.query(Proxy)
    if status:
        query = query.filter(Proxy.status == status)
    if type:
        query = query.filter(Proxy.type == type)
    proxies = query.order_by(Proxy.id.desc()).offset(offset).limit(limit).all()
    return [serialize_proxy(proxy) for proxy in proxies]


@router.post("", response_model=ProxyRead)
def create_proxy_endpoint(payload: ProxyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return serialize_proxy(create_proxy(db, payload, current_user))


@router.get("/{proxy_id}", response_model=ProxyRead)
def read_proxy(proxy_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return serialize_proxy(get_proxy_or_404(db, proxy_id))


@router.put("/{proxy_id}", response_model=ProxyRead)
def update_proxy_endpoint(proxy_id: int, payload: ProxyUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return serialize_proxy(update_proxy(db, get_proxy_or_404(db, proxy_id), payload, current_user))


@router.delete("/{proxy_id}")
def delete_proxy(proxy_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    proxy = get_proxy_or_404(db, proxy_id)
    in_use = db.query(TelegramAccount).filter(TelegramAccount.proxy_id == proxy_id).first()
    if in_use:
        raise HTTPException(status_code=409, detail="Proxy is used by one or more accounts")
    db.delete(proxy)
    db.commit()
    write_audit_log(db, current_user, "proxy.delete", "Proxy", str(proxy_id))
    return {"ok": True}


@router.post("/{proxy_id}/check", response_model=ProxyRead)
def check_proxy_endpoint(proxy_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return serialize_proxy(check_proxy(db, get_proxy_or_404(db, proxy_id), current_user))
