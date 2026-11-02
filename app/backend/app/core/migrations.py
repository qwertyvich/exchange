from sqlalchemy import text

from app.core.database import engine


def run_sqlite_migrations() -> None:
    """Tiny MVP migrations for SQLite schema drift during local development."""
    with engine.begin() as connection:
        template_columns = {
            row[1] for row in connection.execute(text("PRAGMA table_info(templates)")).fetchall()
        }
        if template_columns and "type" not in template_columns:
            connection.execute(text("ALTER TABLE templates ADD COLUMN type VARCHAR(80) NOT NULL DEFAULT 'generic'"))
        if template_columns and "body" not in template_columns:
            connection.execute(text("ALTER TABLE templates ADD COLUMN body TEXT NOT NULL DEFAULT ''"))
            if "content" in template_columns:
                connection.execute(text("UPDATE templates SET body = content WHERE body = ''"))
        if template_columns and "locale" not in template_columns:
            connection.execute(text("ALTER TABLE templates ADD COLUMN locale VARCHAR(16)"))
        if template_columns and "owner_user_id" not in template_columns:
            connection.execute(text("ALTER TABLE templates ADD COLUMN owner_user_id INTEGER"))
            admin_id = connection.execute(text("SELECT id FROM users ORDER BY id LIMIT 1")).scalar()
            if admin_id is not None:
                connection.execute(
                    text("UPDATE templates SET owner_user_id = :admin_id WHERE owner_user_id IS NULL"),
                    {"admin_id": admin_id},
                )
        if template_columns and "type" in template_columns:
            connection.execute(text("UPDATE templates SET type = 'generic' WHERE type = 'message'"))

        settings_columns = {
            row[1] for row in connection.execute(text("PRAGMA table_info(app_settings)")).fetchall()
        }
        if settings_columns and "encrypted_global_api_hash" not in settings_columns:
            connection.execute(text("ALTER TABLE app_settings ADD COLUMN encrypted_global_api_hash VARCHAR(512)"))
            if "global_api_hash_secret" in settings_columns:
                connection.execute(
                    text("UPDATE app_settings SET encrypted_global_api_hash = global_api_hash_secret WHERE encrypted_global_api_hash IS NULL")
                )
        if settings_columns and "default_online_ping_minutes" not in settings_columns:
            connection.execute(text("ALTER TABLE app_settings ADD COLUMN default_online_ping_minutes INTEGER NOT NULL DEFAULT 5"))
            if "default_online_ping_interval" in settings_columns:
                connection.execute(
                    text(
                        "UPDATE app_settings SET default_online_ping_minutes = MAX(1, CAST(default_online_ping_interval / 60 AS INTEGER))"
                    )
                )
        if settings_columns and "message_rate_limit_per_minute" not in settings_columns:
            connection.execute(text("ALTER TABLE app_settings ADD COLUMN message_rate_limit_per_minute INTEGER NOT NULL DEFAULT 5"))

        account_columns = {
            row[1] for row in connection.execute(text("PRAGMA table_info(telegram_accounts)")).fetchall()
        }
        if account_columns and "individual_api_id" not in account_columns:
            connection.execute(text("ALTER TABLE telegram_accounts ADD COLUMN individual_api_id INTEGER"))
            if "api_id_override" in account_columns:
                connection.execute(text("UPDATE telegram_accounts SET individual_api_id = api_id_override WHERE individual_api_id IS NULL"))
        if account_columns and "encrypted_individual_api_hash" not in account_columns:
            connection.execute(text("ALTER TABLE telegram_accounts ADD COLUMN encrypted_individual_api_hash VARCHAR(512)"))
            if "api_hash_secret_override" in account_columns:
                connection.execute(
                    text(
                        "UPDATE telegram_accounts SET encrypted_individual_api_hash = api_hash_secret_override WHERE encrypted_individual_api_hash IS NULL"
                    )
                )
        if account_columns and "online_keepalive_enabled" not in account_columns:
            connection.execute(text("ALTER TABLE telegram_accounts ADD COLUMN online_keepalive_enabled BOOLEAN NOT NULL DEFAULT 0"))
            if "online_keepalive" in account_columns:
                connection.execute(text("UPDATE telegram_accounts SET online_keepalive_enabled = online_keepalive"))
        if account_columns and "online_ping_interval_minutes" not in account_columns:
            connection.execute(text("ALTER TABLE telegram_accounts ADD COLUMN online_ping_interval_minutes INTEGER NOT NULL DEFAULT 15"))

        proxy_columns = {
            row[1] for row in connection.execute(text("PRAGMA table_info(proxies)")).fetchall()
        }
        if proxy_columns and "encrypted_password" not in proxy_columns:
            connection.execute(text("ALTER TABLE proxies ADD COLUMN encrypted_password VARCHAR(512)"))
            if "password_secret" in proxy_columns:
                connection.execute(text("UPDATE proxies SET encrypted_password = password_secret WHERE encrypted_password IS NULL"))
        if proxy_columns and "last_error" not in proxy_columns:
            connection.execute(text("ALTER TABLE proxies ADD COLUMN last_error TEXT"))

        scheduled_columns = {
            row[1] for row in connection.execute(text("PRAGMA table_info(scheduled_actions)")).fetchall()
        }
        if scheduled_columns and "owner_user_id" not in scheduled_columns:
            connection.execute(text("ALTER TABLE scheduled_actions ADD COLUMN owner_user_id INTEGER"))
            if "created_by_user_id" in scheduled_columns:
                connection.execute(
                    text("UPDATE scheduled_actions SET owner_user_id = created_by_user_id WHERE owner_user_id IS NULL")
                )
        if scheduled_columns and "telegram_account_id" not in scheduled_columns:
            connection.execute(text("ALTER TABLE scheduled_actions ADD COLUMN telegram_account_id INTEGER"))
            if "account_id" in scheduled_columns:
                connection.execute(
                    text("UPDATE scheduled_actions SET telegram_account_id = account_id WHERE telegram_account_id IS NULL")
                )
        if scheduled_columns and "scheduled_for" not in scheduled_columns:
            connection.execute(text("ALTER TABLE scheduled_actions ADD COLUMN scheduled_for DATETIME"))
            if "run_at" in scheduled_columns:
                connection.execute(
                    text("UPDATE scheduled_actions SET scheduled_for = run_at WHERE scheduled_for IS NULL")
                )
        if scheduled_columns and "result_json" not in scheduled_columns:
            connection.execute(text("ALTER TABLE scheduled_actions ADD COLUMN result_json TEXT"))
        if scheduled_columns and "error" not in scheduled_columns:
            connection.execute(text("ALTER TABLE scheduled_actions ADD COLUMN error TEXT"))
