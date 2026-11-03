import hmac
import hashlib
import os

# хранить в env, НЕ в коде
TICKET_ACTION_SECRET = os.environ["TICKET_ACTION_SECRET"]

def make_ticket_key(ticket_id: str) -> str:
    
    mac = hmac.new(
        TICKET_ACTION_SECRET.encode("utf-8"),
        ticket_id.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    # можно укоротить, но лучше так
    return mac

def verify_ticket_key(ticket_id: str, key: str) -> bool:
    # constant-time compare
    expected = make_ticket_key(ticket_id)
    return hmac.compare_digest(expected, key or "")
