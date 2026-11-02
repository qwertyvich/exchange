import socket
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.proxy import Proxy, ProxyStatus
from app.models.user import User
from app.schemas.proxies import ProxyCreate, ProxyUpdate
from app.services.audit_service import write_audit_log
from app.storage.secrets import SecretStorage


def serialize_proxy(proxy: Proxy) -> dict:
    return {
        "id": proxy.id,
        "name": proxy.name,
        "type": proxy.type.value,
        "host": proxy.host,
        "port": proxy.port,
        "username": proxy.username,
        "password_masked": SecretStorage.mask(proxy.encrypted_password),
        "status": proxy.status.value,
        "last_checked_at": proxy.last_checked_at,
        "last_error": proxy.last_error,
    }


def create_proxy(db: Session, payload: ProxyCreate, user: User) -> Proxy:
    data = payload.model_dump()
    password = data.pop("password", None)
    proxy = Proxy(**data, encrypted_password=SecretStorage.store(password))
    db.add(proxy)
    db.commit()
    db.refresh(proxy)
    write_audit_log(db, user, "proxy.create", "Proxy", str(proxy.id))
    return proxy


def update_proxy(db: Session, proxy: Proxy, payload: ProxyUpdate, user: User) -> Proxy:
    data = payload.model_dump(exclude_unset=True)
    password = data.pop("password", None)
    for key, value in data.items():
        setattr(proxy, key, value)
    if password is not None:
        proxy.encrypted_password = SecretStorage.store(password)
    db.commit()
    db.refresh(proxy)
    write_audit_log(db, user, "proxy.update", "Proxy", str(proxy.id))
    return proxy


def check_proxy(db: Session, proxy: Proxy, user: User) -> Proxy:
    try:
        with socket.create_connection((proxy.host, proxy.port), timeout=5):
            proxy.status = ProxyStatus.working
            proxy.last_error = None
    except OSError as exc:
        proxy.status = ProxyStatus.failed
        proxy.last_error = f"{exc.__class__.__name__}: {exc}"
    proxy.last_checked_at = datetime.utcnow()
    db.commit()
    db.refresh(proxy)
    write_audit_log(db, user, "proxy.check", "Proxy", str(proxy.id), f"status={proxy.status.value}")
    return proxy
