"""Shared settings/reviews/cache documents stored in PostgreSQL, rather than worker globals."""
from .db import SessionLocal
from .models import SiteDocument


def read_document(key, default=None):
    with SessionLocal() as db:
        row = db.get(SiteDocument, key)
        return row.value if row else default


def write_document(key, value):
    with SessionLocal() as db:
        row = db.get(SiteDocument, key)
        if row:
            row.value = value
        else:
            db.add(SiteDocument(key=key, value=value))
        db.commit()
