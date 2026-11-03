import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL = os.environ["DATABASE_URL"]

# check_same_thread=False нужен для sqlite при работе из веб-сервера
engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    **({"connect_args": {"check_same_thread": False}} if DB_URL.startswith("sqlite") else {"pool_size": 10, "max_overflow": 10}),
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass
