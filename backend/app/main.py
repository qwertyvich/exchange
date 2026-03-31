
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from aiogram import Bot
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
from .settings_loader import load_settings, reset_settings_cache





settings = load_settings()
SETTINGS_PATH = Path(__file__).resolve().parent / "settings.json"
deposit_wallets = settings["deposit_wallets"] 

with SETTINGS_PATH.open("r", encoding="utf-8") as f:
    data = json.load(f)

API_TOKEN = data.get("bot", {}).get("API_TOKEN")#"8231371926:AAG0lIEFcfxB6GsnXllgzi2hdTVjyfZ3wDQ"
CHAT_ID = int(data.get("bot", {}).get("CHAT_ID"))     #чат тикетов
MESS_CHAT = int(data.get("bot", {}).get("MESS_CHAT"))        #чат отстуков
bot = Bot(token=API_TOKEN)
domain = data.get("bot", {}).get("domain") 

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

app = FastAPI()

class ContactPayload(BaseModel):
    username: str
    message: str

@app.get("/api/settings/public")
def public_settings():
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
        }


Base.metadata.create_all(bind=engine)


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


@app.on_event("shutdown")
async def shutdown():
    await bot.session.close()


@app.post("/api/ask")
async def ask(payload: ContactPayload):
    try:
        await bot.send_message(
            MESS_CHAT,
            f"<b>✉️Сообщение</b>\n\n<b>От: {payload.username}</b>\n{payload.message}",
            parse_mode="HTML",
        )
    except Exception:
        pass
    return {"status": "sent"}


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

    if user:
        # пользователь залогинен — тикет сразу его
        t = create_ticket(db, payload, guest_id=None, user_id=user.id)
    else:
        # без логина — по guest_id
        gid = ensure_guest_id(request, response)
        t = create_ticket(db, payload, guest_id=gid, user_id=None)
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
            f"<b> <blockquote>{moneta[t.give_currency_backend_id]} -> {moneta[t.get_currency_backend_id]}</blockquote></b>\n\n"+
            f"<b>┏ К обмену: {moneta[t.give_currency_backend_id]}</b>\n"+
            f"{price_line}"+
            f"<b>┗ Сумма: {t.give_amount} {t.give_symbol}\n</b>\n"+
            f"<b>┏ К получению: {moneta[t.get_currency_backend_id]}</b>\n"+
            f"<b>┗ Сумма: {t.get_amount} {t.get_symbol}\n</b>\n"+
            f"<b>👤Клиент:</b>\n"+
            f"<b>┏Telegram: {t.telegram}</b>\n"+
            f"<b>┗Счёт: {t.payout_details}</b>\n\n"+
            f"<b>Адрес отправки: {deposit_wallets[str(t.give_currency_backend_id)]['address']}</b>\n"+
            f"<b>Комиссия: {t.fee_percent}%</b>\n\n",
            parse_mode="HTML",
        )
        await bot.send_message(
            CHAT_ID,
            f"<b>👆🏻{moneta[t.get_currency_backend_id]} </b>\n"+ 
            f"<b><pre>{t.payout_details}</pre></b>\n"+
            f"<b><pre>{t.get_amount}</pre></b>\n"+
            f"<a href=\"{domain}/api/tickets/{t.id}?key={make_ticket_key(t.id)}&action=cancel\"><b>❌Отменить сделку</b></a>\n"+
            f"<a href=\"{domain}/api/tickets/{t.id}?key={make_ticket_key(t.id)}&action=complete\"><b>✅Подтвердить перевод</b></a>",
            parse_mode="HTML",
        )
        
    except Exception as e:
        print(e)
    return {"ok": True, "ticket_id": t.id, "url": f"/tickets/{t.id}", "status": t.status}


@app.get("/api/tickets/{ticket_id}")
async def api_get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    key: str | None = Query(default=None),
    action: str | None = Query(default=None, pattern="^(cancel|complete)$"),
):
    t = get_ticket(db, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="ticket not found")
    
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
async def cancel_ticket(ticket_id: str, db: Session = Depends(get_db)):
    t = get_ticket(db, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="ticket not found")

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
    receipt: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    t = get_ticket(db, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="ticket not found")

    if t.status in ("cancelled", "completed"):
        raise HTTPException(status_code=400, detail="cannot confirm this ticket")

    try:
        await bot.send_message(
            CHAT_ID,
            f"<b>📄 Тикет #{t.id} </b>\n"
            f"<b>✅Перевод подтвержден клиентом</b>\n"
            "----------------------\n"
            f"<a href=\"{domain}/api/tickets/{t.id}?key={make_ticket_key(t.id)}&action=cancel\"><b>❌Отменить сделку\n</b></a>"
            f"<a href=\"{domain}/api/tickets/{t.id}?key={make_ticket_key(t.id)}&action=complete\"><b>✅Подтвердить перевод</b></a>",
            parse_mode="HTML",
        )

        # если прикрепили чек — шлём его отдельным сообщением
        if receipt is not None:
            content = await receipt.read()

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

    except Exception as e:
        print("confirm tg error:", e)

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
            secure=False,  # на https поставишь True
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

    SETTINGS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    reset_settings_cache()
    return {"ok": True, "settings": load_settings()}


@app.get("/api/reviews/public", response_model=List[ReviewOut])
def public_reviews():
    path = Path(__file__).resolve().parent / "reviews.json"

    if not path.exists():
        return []

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        raise HTTPException(status_code=500, detail="failed to read reviews")

    if not isinstance(raw, list):
        raise HTTPException(status_code=500, detail="reviews must be a JSON array")

    result = []
    for item in raw:
        if not isinstance(item, dict):
            continue

        name = str(item.get("name", "")).strip()
        text = str(item.get("text", "")).strip()

        try:
            mark = int(item.get("mark", 0))
        except Exception:
            mark = 0

        if not name or not text:
            continue

        if mark < 1:
            mark = 1
        if mark > 5:
            mark = 5

        result.append({
            "name": name,
            "text": text,
            "mark": mark,
        })

    return result    