from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import accounts, admin, audit_logs, auth, proxies, scheduled_actions, settings, templates
from app.core.database import Base, SessionLocal, engine
from app.core.migrations import run_sqlite_migrations
from app.models import *  # noqa: F403
from app.services.auth_service import bootstrap_admin
from app.services.scheduler_service import shutdown_scheduler, start_scheduler

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    run_sqlite_migrations()
    db = SessionLocal()
    try:
        bootstrap_admin(db)
    finally:
        db.close()
    start_scheduler()
    yield
    shutdown_scheduler()


app = FastAPI(title="Telegram Account Panel MVP", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(settings.router, prefix="/api")
app.include_router(accounts.router, prefix="/api")
app.include_router(proxies.router, prefix="/api")
app.include_router(templates.router, prefix="/api")
app.include_router(scheduled_actions.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(audit_logs.router, prefix="/api")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": "Validation error", "errors": exc.errors()}),
    )
