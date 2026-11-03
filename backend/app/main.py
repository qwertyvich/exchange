
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from .notifications import QueuedBot, notification_worker, enabled as telegram_enabled
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import Body
from .security import make_ticket_key, verify_ticket_key
import time
import json
from pathlib import Path
from datetime import timezone
from fastapi import Request, Response
import secrets
from .schemas import RegisterIn, LoginIn, UserOut, ReviewOut
from .crud import create_user, get_user_by_email, authenticate_user, attach_tickets_to_user, get_user_by_id, get_user_tickets
from .auth import create_access_token, decode_token, hash_password, verify_password
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .crud import admin_list_users, admin_user_tickets
from fastapi import UploadFile, File, Form
from tempfile import NamedTemporaryFile
import os


from .db import Base, engine, SessionLocal
from .schemas import TicketCreate, TicketOut, Side, Client, RatesSnapshot, ProfileNameIn, ProfilePasswordIn
from .crud import create_ticket, get_ticket
from .settings_loader import load_settings, reset_settings_cache, save_settings
from .settings_validation import validated_settings
from .documents import read_document
from .rates import rate_table, rates_worker, make_quote, decode_quote, CRYPTO
from contextlib import asynccontextmanager
from html import escape
import asyncio
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from .models import Ticket





# Telegram credentials are resolved by the delivery worker, after each admin update.
CHAT_ID = "tickets"
MESS_CHAT = "messages"
bot = QueuedBot()

def public_domain():
    return (os.getenv("PUBLIC_URL") or load_settings().get("bot", {}).get("domain", "http://localhost:5173")).rstrip("/")

@asynccontextmanager
async def lifespan(app):
    tasks = [asyncio.create_task(rates_worker()), asyncio.create_task(notification_worker())]
    yield
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


moneta = {
    1: "Bitcoin",
    2: "Ethereum",
    3: "Tether TRC20",
    4: "Tether ERC20",
    5: "Tether BEP20",
    6: "Tether SOL",
    7: "DAI ERC20",
    8: "USDC ERC20",
    9: "Solana",
    10: "Litecoin",
    11: "TRON",
    12: "Dogecoin",

    2001: "СБП перевод",
    2011: "Сбер QR наличные",
    2002: "Сбер банк",
    2003: "Альфа банк",
    2010: "Наличные",
    2101: "Перевод на карту",
    2102: "Турция",
    2103: "Таиланд",
    2104: "Египет",
    2105: "ОАЭ",
    2106: "Грузия",
    2107: "Армения",
    2108: "Азербайджан",
    2109: "Беларусь",
    2110: "Вьетнам",
    2111: "Индонезия",
    2112: "Шри-Ланка",
    2113: "Индия",
    2114: "Китай",
    2115: "Малайзия",
    2116: "Япония",
    2117: "Южная Корея",
    2118: "Сингапур",
    2119: "Филиппины",
    2120: "Тайвань",
    
}

app = FastAPI(lifespan=lifespan)

class ContactPayload(BaseModel):
    username: str
    message: str

@app.get("/api/settings/public")
def public_settings(response: Response):
    response.headers["Cache-Control"] = "public, max-age=10"
    s = load_settings()
    # отдаём только то, что можно публично
    return {
        "banner": s.get("banner", ""),
        "percent": s.get("percent", 0), 
        "giveMin": s.get("giveMin"),
        "giveMax": s.get("giveMax"),
        "getMin": s.get("getMin"),
        "getMax": s.get("getMax"),
        "deposit_wallets": s.get("deposit_wallets", {}),
        "info": s.get("info", {}),
        "mode": s.get("mode", "0"),
        "fiat_in": s.get("fiat_in", {}),
        "fiat_out": s.get("fiat_out", {}),
        "fiat_in_methods": s.get("fiat_in_methods", {}),
        "direction_rates": s.get("direction_rates", {}),
        }


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "database": engine.dialect.name}

@app.get("/api/rates")
def public_rates(response: Response):
    response.headers["Cache-Control"] = "public, max-age=10"
    return rate_table(load_settings())

class QuoteIn(BaseModel):
    give_id: int
    get_id: int
    amount: str

@app.post("/api/quote")
def quote(payload: QuoteIn, request: Request, response: Response):
    try:
        result = make_quote(load_settings(), payload.give_id, payload.get_id, payload.amount)
        ensure_guest_id(request, response)
        return result
    except (ValueError, ArithmeticError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))



class ContactPayload(BaseModel):
    username: str
    message: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bearer = HTTPBearer(auto_error=False)

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    if not creds:
        return None
    user_id = decode_token(creds.credentials)
    if not user_id:
        return None
    return get_user_by_id(db, user_id)


@app.post("/api/ask")
async def ask(payload: ContactPayload):
    try:
        await bot.send_message(
            MESS_CHAT,
            f"<b>✉️Сообщение</b>\n\n<b>От: {escape(payload.username)}</b>\n{escape(payload.message)}",
            parse_mode="HTML",
        )
    except Exception:
        pass
    return {"status": "queued" if telegram_enabled() else "disabled"}


@app.post("/api/tickets", response_model=dict)
async def create_ticket_endpoint(
                        payload: TicketCreate,
                        request: Request,
                        response: Response,
                        db: Session = Depends(get_db),
                        user=Depends(get_current_user),
                    ):
    #print("AUTH HEADER:", request.headers.get("authorization"))
    #print("USER:", getattr(user, "id", None))
    
    if not payload.client.telegram.strip():
        raise HTTPException(status_code=400, detail="telegram is required")
    if not payload.client.payout_details.strip():
        raise HTTPException(status_code=400, detail="payout_details is required")

    if payload.get_is_fiat and not payload.fiat_code:
        raise HTTPException(status_code=400, detail="fiat_code is required for fiat payout")

    try:
        locked = decode_quote(payload.quote_token)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    if locked["give_id"] != payload.give.currency_backend_id or locked["get_id"] != payload.get.currency_backend_id:
        raise HTTPException(status_code=400, detail="Направление не совпадает с расчётом")
    payload.give.amount = Decimal(locked["give_amount"])
    payload.get.amount = Decimal(locked["get_amount"])
    payload.give.symbol = locked["give_symbol"]
    payload.get.symbol = locked["get_symbol"]
    payload.give.coingecko_id = CRYPTO.get(locked["give_id"], (None,))[0]
    payload.get.coingecko_id = CRYPTO.get(locked["get_id"], (None,))[0]
    payload.fee_percent = locked["fee_percent"]
    payload.get_is_fiat = locked["get_id"] not in CRYPTO
    payload.fiat_code = payload.get.symbol.lower() if payload.get_is_fiat else None
    payload.rates_snapshot = RatesSnapshot()
    payload.quote_id = locked["jti"]
    existing = db.query(Ticket).filter_by(quote_id=payload.quote_id).first()
    if existing:
        require_ticket_access(existing, request, user)
        return {"ok": True, "ticket_id": existing.id, "url": f"/tickets/{existing.id}", "status": existing.status}

    try:
        if user:
            t = create_ticket(db, payload, guest_id=None, user_id=user.id)
        else:
            gid = ensure_guest_id(request, response)
            t = create_ticket(db, payload, guest_id=gid, user_id=None)
    except IntegrityError:
        db.rollback()
        existing = db.query(Ticket).filter_by(quote_id=payload.quote_id).first()
        if not existing:
            raise
        require_ticket_access(existing, request, user)
        return {"ok": True, "ticket_id": existing.id, "url": f"/tickets/{existing.id}", "status": existing.status}
    if t.give_usd is not None and t.give_rub is not None:
        price_line = f"<b>┣ Цена за 1 {t.give_symbol}: {round(t.give_usd)} $ | {t.give_rub} ₽\n</b>"
    elif t.give_rub is not None:
        price_line = f"<b>┣ Курс: {t.give_rub} RUB за 1 USD\n</b>"
    else:
        price_line = ""
    try:
        await bot.send_message(
            CHAT_ID,
            f"<b>📄 Тикет #{t.id} </b>\n"+
            f"<b> <blockquote>{escape(moneta.get(t.give_currency_backend_id, t.give_symbol))} -> {escape(moneta.get(t.get_currency_backend_id, t.get_symbol))}</blockquote></b>\n\n"+
            f"<b>┏ К обмену: {escape(moneta.get(t.give_currency_backend_id, t.give_symbol))}</b>\n"+
            f"{price_line}"+
            f"<b>┗ Сумма: {t.give_amount} {t.give_symbol}\n</b>\n"+
            f"<b>┏ К получению: {escape(moneta.get(t.get_currency_backend_id, t.get_symbol))}</b>\n"+
            f"<b>┗ Сумма: {t.get_amount} {t.get_symbol}\n</b>\n"+
            f"<b>👤Клиент:</b>\n"+
            f"<b>┏Telegram: {escape(t.telegram)}</b>\n"+
            f"<b>┗Счёт: {escape(t.payout_details)}</b>\n\n"+
            f"<b>Адрес отправки: {escape(str(load_settings().get('deposit_wallets', {}).get(str(t.give_currency_backend_id), {}).get('address', 'См. реквизиты заявки')))}</b>\n"+
            f"<b>Комиссия: {t.fee_percent}%</b>\n\n",
            parse_mode="HTML",
        )
        await bot.send_message(
            CHAT_ID,
            f"<b>👆🏻{escape(moneta.get(t.get_currency_backend_id, t.get_symbol))} </b>\n"+
            f"<b><pre>{escape(t.payout_details)}</pre></b>\n"+
            f"<b><pre>{t.get_amount}</pre></b>\n"+
            f"<a href=\"{public_domain()}/api/tickets/{t.id}?key={make_ticket_key(t.id)}&action=cancel\"><b>❌Отменить сделку</b></a>\n"+
            f"<a href=\"{public_domain()}/api/tickets/{t.id}?key={make_ticket_key(t.id)}&action=complete\"><b>✅Подтвердить перевод</b></a>",
            parse_mode="HTML",
        )
        
    except Exception as e:
        print(e)
    return {"ok": True, "ticket_id": t.id, "url": f"/tickets/{t.id}", "status": t.status}


@app.get("/api/tickets/{ticket_id}")
async def api_get_ticket(
    ticket_id: str,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    key: str | None = Query(default=None),
    action: str | None = Query(default=None, pattern="^(cancel|complete)$"),
):
    t = get_ticket(db, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="ticket not found")
    
    if not action:
        require_ticket_access(t, request, user)
    if action:
        if not key:
            raise HTTPException(status_code=403, detail="key is required")

        if not verify_ticket_key(ticket_id, key):
            raise HTTPException(status_code=403, detail="invalid key")

        # защита от повторного изменения
        if t.status in ("cancelled", "completed"):
            raise HTTPException(status_code=400, detail="ticket already closed")

        if action == "cancel":
            t.status = "cancelled"
            await bot.send_message(
                CHAT_ID,
                f"<b>📄 Тикет #{t.id} </b>\n"+
                f"<b>❌Отменён</b>\n",
                parse_mode="HTML",
            )
            
        elif action == "complete":
            t.status = "completed"
            await bot.send_message(
                CHAT_ID,
                f"<b>📄 Тикет #{t.id} </b>\n"+
                f"<b>✅Подтвержден</b>\n",
                parse_mode="HTML",
            )

        db.commit()
        db.refresh(t)
    #cюда логику
    return {
        "id": t.id,
        "status": t.status,
        "give": {
            "currency_backend_id": t.give_currency_backend_id,
            "coingecko_id": t.give_coingecko_id,
            "symbol": t.give_symbol,
            "amount": t.give_amount,
        },
        "get": {
            "currency_backend_id": t.get_currency_backend_id,
            "coingecko_id": t.get_coingecko_id,
            "symbol": t.get_symbol,
            "amount": t.get_amount,
        },
        "fee_percent": t.fee_percent,
        "client": {"telegram": t.telegram, "payout_details": t.payout_details},
        "rates_snapshot": {"give_usd": t.give_usd, "give_rub": t.give_rub, "get_usd": t.get_usd},
        "created_at": t.created_at.replace(tzinfo=timezone.utc).isoformat(),
    }

@app.patch("/api/tickets/{ticket_id}/cancel")
async def cancel_ticket(ticket_id: str, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = get_ticket(db, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="ticket not found")

    require_ticket_access(t, request, user)
    # если уже завершён — можно запретить (по желанию)
    if t.status == "completed":
        raise HTTPException(status_code=400, detail="cannot cancel completed ticket")
    await bot.send_message(
        CHAT_ID,
        f"<b>📄 Тикет #{t.id} </b>\n"+
        f"<b>❌Отменён клиентом</b>\n",
        parse_mode="HTML",
    )
    t.status = "cancelled"
    db.add(t)
    db.commit()
    db.refresh(t)

    return {"ok": True, "ticket_id": t.id, "status": t.status}

@app.patch("/api/tickets/{ticket_id}/confirm")
async def confirm_ticket(
    ticket_id: str,
    request: Request,
    user=Depends(get_current_user),
    receipt: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    t = get_ticket(db, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="ticket not found")

    require_ticket_access(t, request, user)
    if t.status in ("cancelled", "completed"):
        raise HTTPException(status_code=400, detail="cannot confirm this ticket")

    try:
        await bot.send_message(
            CHAT_ID,
            f"<b>📄 Тикет #{t.id} </b>\n"
            f"<b>✅Перевод подтвержден клиентом</b>\n"
            "----------------------\n"
            f"<a href=\"{public_domain()}/api/tickets/{t.id}?key={make_ticket_key(t.id)}&action=cancel\"><b>❌Отменить сделку\n</b></a>"
            f"<a href=\"{public_domain()}/api/tickets/{t.id}?key={make_ticket_key(t.id)}&action=complete\"><b>✅Подтвердить перевод</b></a>",
            parse_mode="HTML",
        )

        # если прикрепили чек — шлём его отдельным сообщением
        if receipt is not None:
            content = await receipt.read(10 * 1024 * 1024 + 1)
            if len(content) > 10 * 1024 * 1024:
                raise HTTPException(status_code=413, detail="Чек не должен превышать 10 МБ")

            if content:
                suffix = os.path.splitext(receipt.filename or "")[1] or ".jpg"

                with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(content)
                    tmp_path = tmp.name

                try:
                    from aiogram.types import FSInputFile

                    photo = FSInputFile(tmp_path)
                    await bot.send_photo(
                        CHAT_ID,
                        photo=photo,
                        caption=f"🧾 Чек по тикету #{t.id}",
                    )
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

    except HTTPException:
        raise
    except Exception as e:
        print("confirm notification queue error:", type(e).__name__)

    t.status = "not_confirmed"
    db.add(t)
    db.commit()
    db.refresh(t)

    return {"ok": True, "ticket_id": t.id, "status": t.status}

    #"cancelled", "completed" от бота будут идти

def ensure_guest_id(request: Request, response: Response) -> str:
    gid = request.cookies.get("guest_id")
    if not gid:
        gid = secrets.token_hex(16)
        response.set_cookie(
            "guest_id",
            gid,
            httponly=True,
            samesite="lax",
            secure=os.getenv("PUBLIC_URL", "").startswith("https://"),
            max_age=60 * 60 * 24 * 30,
        )
    return gid

@app.post("/api/registration")
def registration(payload: RegisterIn, db: Session = Depends(get_db)):
    try:
        if get_user_by_email(db, payload.email):
            raise HTTPException(status_code=400, detail="email already exists")

        if len(payload.name.strip()) < 4:
            raise HTTPException(status_code=400, detail="name too short")
        if len(payload.name.strip()) > 10:
            raise HTTPException(status_code=400, detail="name too long")
        if len(payload.password) < 8:
            raise HTTPException(status_code=400, detail="password too short")

        u = create_user(db, payload.name.strip(), payload.email, payload.password)
        return {"ok": True, "user_id": u.id}

    except HTTPException:
        raise
    except Exception as e:
        # ВРЕМЕННО для отладки
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login")
def login(payload: LoginIn, request: Request, response: Response, db: Session = Depends(get_db)):
    u = authenticate_user(db, payload.email, payload.password)
    if not u:
        raise HTTPException(status_code=401, detail="invalid credentials")

    # обновляем last_login_at
    u.last_login_at = datetime.utcnow()
    db.add(u)
    db.commit()
    db.refresh(u)

    # привязываем тикеты созданные до логина
    gid = ensure_guest_id(request, response)
    attach_tickets_to_user(db, u.id, gid)

    token = create_access_token(u.id)

    # можешь хранить токен в httpOnly cookie (безопаснее), но фронт проще с JSON
    return {
        "ok": True,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "is_superuser": u.is_superuser,
            "created_at": u.created_at.isoformat() + "Z",
            "last_login_at": u.last_login_at.isoformat() + "Z" if u.last_login_at else None,
        },
    }

@app.get("/api/me")
def me(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="not authenticated")
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role, "is_superuser": user.is_superuser}


@app.get("/api/my/tickets")
def my_tickets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="not authenticated")

    tickets = get_user_tickets(db, user.id)
    return [
        {
            "id": t.id,
            "status": t.status,
            "created_at": t.created_at.replace(tzinfo=timezone.utc).isoformat(),

            "give_currency_backend_id": t.give_currency_backend_id,
            "get_currency_backend_id": t.get_currency_backend_id,

            "give_symbol": t.give_symbol,
            "give_amount": t.give_amount,
            "get_symbol": t.get_symbol,
            "get_amount": t.get_amount,
        }
        for t in tickets
    ]


@app.patch("/api/profile/name")
def profile_update_name(payload: ProfileNameIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="not authenticated")

    name = payload.name.strip()
    if len(name) < 4:
        raise HTTPException(status_code=400, detail="name too short")
    if len(name) > 10:
        raise HTTPException(status_code=400, detail="name too long")

    user.name = name
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"ok": True, "name": user.name}

@app.patch("/api/profile/password")
def profile_update_password(payload: ProfilePasswordIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="not authenticated")

    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="wrong current password")

    if len(payload.new_password) < 8:
        raise HTTPException(status_code=400, detail="password too short")

    if payload.new_password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="passwords do not match")

    user.password_hash = hash_password(payload.new_password)
    db.add(user)
    db.commit()

    return {"ok": True}


@app.get("/api/admin/users")
def admin_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user or not user.is_superuser:
        raise HTTPException(status_code=403, detail="forbidden")

    users = admin_list_users(db)
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "is_superuser": u.is_superuser,
            "created_at": u.created_at.replace(tzinfo=timezone.utc).isoformat() if u.created_at else None,
            "last_login_at": u.last_login_at.replace(tzinfo=timezone.utc).isoformat() if u.last_login_at else None,
        }
        for u in users
    ]


@app.get("/api/admin/users/{user_id}/tickets")
def admin_users_tickets(user_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user or not user.is_superuser:
        raise HTTPException(status_code=403, detail="forbidden")

    tickets = admin_user_tickets(db, user_id)
    return [
        {
            "id": t.id,
            "status": t.status,
            "created_at": t.created_at.replace(tzinfo=timezone.utc).isoformat(),

            "give_currency_backend_id": t.give_currency_backend_id,
            "get_currency_backend_id": t.get_currency_backend_id,
            "give_symbol": t.give_symbol,
            "give_amount": t.give_amount,
            "get_symbol": t.get_symbol,
            "get_amount": t.get_amount,
        }
        for t in tickets
    ]

@app.get("/api/admin/settings")
def admin_get_settings(user=Depends(get_current_user)):
    if not user or not user.is_superuser:
        raise HTTPException(status_code=403, detail="forbidden")
    return load_settings(force=True)

@app.put("/api/admin/settings")
async def admin_put_settings(request: Request, user=Depends(get_current_user)):
    if not user or not user.is_superuser:
        raise HTTPException(status_code=403, detail="forbidden")

    data = await request.json()  # <-- просто принимаем любой JSON

    # (необязательно, но полезно) минимальная проверка, что это объект
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="settings must be a JSON object")

    try:
        merged = validated_settings(load_settings(), data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    save_settings(merged)
    return {"ok": True, "settings": merged}


@app.get("/api/reviews/public", response_model=List[ReviewOut])
def public_reviews(response: Response):
    response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=300"
    return read_document("reviews", [])


def require_ticket_access(ticket, request, user):
    if user and (user.is_superuser or ticket.user_id == user.id):
        return
    if ticket.guest_id and secrets.compare_digest(ticket.guest_id, request.cookies.get("guest_id", "")):
        return
    raise HTTPException(status_code=404, detail="ticket not found")
