from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Side(BaseModel):
    currency_backend_id: int
    coingecko_id: Optional[str] = None
    symbol: str
    amount: float

class Client(BaseModel):
    telegram: str
    payout_details: str

class RatesSnapshot(BaseModel):
    give_usd: Optional[float] = None
    give_rub: Optional[float] = None
    get_usd: Optional[float] = None

class TicketCreate(BaseModel):
    give: Side
    get: Side
    fee_percent: float = Field(ge=0, le=100)

    get_is_fiat: bool = False
    fiat_code: Optional[str] = None
    rub_kind: Optional[str] = None

    client: Client
    rates_snapshot: RatesSnapshot
    created_at: str

class TicketOut(BaseModel):
    id: str
    status: str
    give: Side
    get: Side
    fee_percent: float
    client: Client
    rates_snapshot: RatesSnapshot
    created_at: str

class RegisterIn(BaseModel):
    name: str = Field(min_length=4, max_length=10)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role: str
    is_superuser: bool
    created_at: str
    last_login_at: str | None

class ProfileNameIn(BaseModel):
    name: str

class ProfilePasswordIn(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str