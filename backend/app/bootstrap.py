"""Idempotent legacy import. Never overwrites later changes."""
import json
import os
from pathlib import Path
from sqlalchemy import create_engine, select, MetaData, Table
from .db import SessionLocal
from .models import User, Ticket, SiteDocument
from .auth import hash_password


def bootstrap():
    with SessionLocal() as db:
        if not db.get(SiteDocument, "legacy_imported"):
            legacy_path = Path(os.getenv("LEGACY_SQLITE_PATH", "/app/changer.db.db"))
            if legacy_path.is_file():
                source = create_engine(f"sqlite:///{legacy_path}")
                with source.connect() as conn:
                    for model in (User, Ticket):
                        source_table = Table(model.__tablename__, MetaData(), autoload_with=conn)
                        for row in conn.execute(select(source_table)).mappings():
                            row = dict(row)
                            # SQLite reflection supplies datetimes/booleans too; missing new columns stay NULL.
                            if db.get(model, row["id"]) is None:
                                db.add(model(**row))
                source.dispose()
            base = Path(__file__).parent
            for key, filename in (("settings", "settings.json"), ("reviews", "reviews.json")):
                if not db.get(SiteDocument, key):
                    db.add(SiteDocument(key=key, value=json.loads((base / filename).read_text())))
            db.add(SiteDocument(key="legacy_imported", value={"done": True}))
            db.commit()
        email = os.getenv("ADMIN_EMAIL", "").strip().lower()
        password = os.getenv("ADMIN_PASSWORD", "")
        if email and password and not db.query(User).filter_by(email=email).first():
            db.add(User(name="Админ", email=email, password_hash=hash_password(password), role="admin", is_superuser=True))
            db.commit()


if __name__ == "__main__":
    bootstrap()
