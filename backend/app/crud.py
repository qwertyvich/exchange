import json
import secrets
from datetime import datetime
from sqlalchemy.orm import Session
from .schemas import TicketCreate
from .models import User, Ticket
from .auth import hash_password, verify_password
from datetime import datetime



def generate_ticket_id() -> str:
    return secrets.token_hex(16)

def create_ticket(db: Session, payload: TicketCreate, guest_id: str | None = None, user_id: str | None = None) -> Ticket:
    ticket_id = generate_ticket_id()
    raw_json = json.dumps(payload.model_dump(), ensure_ascii=False)

    t = Ticket(
        id=ticket_id,
        created_at=datetime.utcnow(),

        give_currency_backend_id=payload.give.currency_backend_id,
        give_symbol=payload.give.symbol,
        give_amount=float(payload.give.amount),
        give_coingecko_id=payload.give.coingecko_id or "",

        get_currency_backend_id=payload.get.currency_backend_id,
        get_symbol=payload.get.symbol,
        get_amount=float(payload.get.amount),
        get_coingecko_id=payload.get.coingecko_id,

        get_is_fiat=bool(payload.get_is_fiat),
        fiat_code=payload.fiat_code,
        rub_kind=payload.rub_kind,

        fee_percent=float(payload.fee_percent),

        telegram=payload.client.telegram,
        payout_details=payload.client.payout_details,

        give_usd=payload.rates_snapshot.give_usd,
        give_rub=payload.rates_snapshot.give_rub,
        get_usd=payload.rates_snapshot.get_usd,

        raw_payload_json=raw_json,
        status="new",
        guest_id=guest_id,
        user_id=user_id,
    )
    
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

def get_ticket(db: Session, ticket_id: str) -> Ticket | None:
    return db.get(Ticket, ticket_id)

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.get(User, user_id)

def create_user(db: Session, name: str, email: str, password: str) -> User:
    u = User(
        name=name,
        email=email.lower().strip(),
        password_hash=hash_password(password),
        created_at=datetime.utcnow(),
        role="user",
        is_superuser=False,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    u = get_user_by_email(db, email.lower().strip())
    if not u:
        return None
    if not verify_password(password, u.password_hash):
        return None
    return u

def attach_tickets_to_user(db: Session, user_id: str, guest_id: str | None):
    if not guest_id:
        return
    db.query(Ticket).filter(Ticket.guest_id == guest_id, Ticket.user_id.is_(None)).update(
        {"user_id": user_id, "guest_id": None},
        synchronize_session=False,
    )
    db.commit()

def get_user_tickets(db: Session, user_id: str) -> list[Ticket]:
    return (
        db.query(Ticket)
        .filter(Ticket.user_id == user_id)
        .order_by(Ticket.created_at.desc())
        .all()
    )

def update_user_name(db: Session, user: User, name: str) -> User:
    user.name = name
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user: User, new_password: str) -> None:
    user.password_hash = hash_password(new_password)
    db.add(user)
    db.commit()

def admin_list_users(db: Session):
    return db.query(User).order_by(User.last_login_at.desc()).all()

def admin_user_tickets(db: Session, user_id: str):
    return (
        db.query(Ticket)
        .filter(Ticket.user_id == user_id)
        .order_by(Ticket.created_at.desc())
        .all()
    )