from datetime import datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.app_settings import AppSettings
from app.models.proxy import Proxy
from app.models.telegram_account import AccountStatus, TelegramAccount
from app.storage.secrets import SecretStorage


class TelethonService:
    """Safe MVP interface for future first-party account operations."""

    def resolve_credentials(self, db: Session, account: TelegramAccount) -> tuple[int, str]:
        if account.individual_api_id and account.encrypted_individual_api_hash:
            api_hash = SecretStorage.reveal(account.encrypted_individual_api_hash)
            if api_hash:
                return account.individual_api_id, api_hash

        settings = db.query(AppSettings).first()
        if settings and settings.global_api_id and settings.encrypted_global_api_hash:
            api_hash = SecretStorage.reveal(settings.encrypted_global_api_hash)
            if api_hash:
                return settings.global_api_id, api_hash

        raise HTTPException(
            status_code=400,
            detail="Telegram API credentials are not configured for this account or globally",
        )

    def build_proxy_connector(self, proxy: Proxy | None) -> dict | None:
        if not proxy:
            return None
        return {
            "type": proxy.type.value,
            "host": proxy.host,
            "port": proxy.port,
            "username": proxy.username,
            "password": SecretStorage.reveal(proxy.encrypted_password),
            "todo": "Wire this into Telethon client creation with the chosen proxy library.",
        }

    def connect_account(self, account: TelegramAccount) -> dict:
        account.last_connected_at = datetime.utcnow()
        account.status = AccountStatus.active
        return {
            "account_id": account.id,
            "status": "not_implemented",
            "todo": "Connect via Telethon using stored session safely.",
        }

    def change_name(self, account: TelegramAccount, first_name: str, last_name: str | None = None) -> dict:
        return {"account_id": account.id, "status": "not_implemented", "first_name": first_name, "last_name": last_name}

    def change_username(self, account: TelegramAccount, username: str) -> dict:
        return {"account_id": account.id, "status": "not_implemented", "username": username}

    def change_bio(self, account: TelegramAccount, bio: str) -> dict:
        return {"account_id": account.id, "status": "not_implemented", "bio_length": len(bio)}

    def upload_profile_photo(self, account: TelegramAccount, file: UploadFile | None = None, file_path: str | None = None) -> dict:
        return {
            "account_id": account.id,
            "status": "not_implemented",
            "file_name": getattr(file, "filename", None),
            "file_path": file_path,
        }

    def keepalive_ping(self, account: TelegramAccount) -> dict:
        account.last_connected_at = datetime.utcnow()
        return {"account_id": account.id, "status": "stub", "last_connected_at": account.last_connected_at.isoformat()}

    def list_dialogs(self, account: TelegramAccount) -> list[dict]:
        return [
            {
                "id": "stub-dialog",
                "title": "Saved Messages",
                "type": "stub",
                "unread_count": 0,
                "last_message": "Telethon integration TODO",
            }
        ]

    def list_messages(self, account: TelegramAccount, dialog_id: str, limit: int = 50, offset: int = 0) -> list[dict]:
        return [
            {
                "id": offset + 1,
                "dialog_id": dialog_id,
                "sender": "system",
                "text": "Message listing is a safe MVP stub until Telethon is wired.",
                "created_at": datetime.utcnow().isoformat(),
            }
        ][:limit]

    def send_message_to_existing_dialog(self, account: TelegramAccount, dialog_id: str, text: str) -> dict:
        return {
            "account_id": account.id,
            "dialog_id": dialog_id,
            "status": "stub",
            "safety": "Only existing dialogs are supported; mass messaging is intentionally not implemented.",
        }

    def send_message_by_username(self, account: TelegramAccount, username: str, text: str, confirmed: bool) -> dict:
        if not confirmed:
            raise HTTPException(status_code=400, detail="Sending by username requires confirmed=true")
        return {
            "account_id": account.id,
            "username": username,
            "status": "stub",
            "safety": "Use only for accounts/users you are allowed to contact.",
        }
