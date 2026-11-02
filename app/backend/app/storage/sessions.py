from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

SESSIONS_DIR = Path(__file__).resolve().parents[2] / "data" / "sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def save_session_file(file: UploadFile) -> str:
    if not file.filename or not file.filename.endswith(".session"):
        raise ValueError("Only .session files are allowed")
    safe_name = f"{uuid4().hex}_{Path(file.filename).name}"
    target = SESSIONS_DIR / safe_name
    with target.open("wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            buffer.write(chunk)
    return safe_name


def delete_session_file(filename: str | None) -> bool:
    if not filename:
        return False
    target = (SESSIONS_DIR / filename).resolve()
    sessions_root = SESSIONS_DIR.resolve()
    if sessions_root not in target.parents:
        return False
    if target.exists() and target.is_file():
        target.unlink()
        return True
    return False
