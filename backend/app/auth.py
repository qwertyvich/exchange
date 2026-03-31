from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

JWT_SECRET = "86429756"  # потом в env
JWT_ALG = "HS256"
ACCESS_MINUTES = 60 * 24 * 7  # 7 дней, можешь меньше


pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _bcrypt_safe(password: str) -> str:
    b = password.encode("utf-8")
    if len(b) > 72:
        b = b[:72]
    return b.decode("utf-8", errors="ignore")

def hash_password(password: str) -> str:
    return pwd.hash(_bcrypt_safe(password))

def verify_password(password: str, password_hash: str) -> bool:
    return pwd.verify(_bcrypt_safe(password), password_hash)
    
def create_access_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return payload.get("sub")
    except JWTError:
        return ""