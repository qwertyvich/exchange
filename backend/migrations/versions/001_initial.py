"""Initial PostgreSQL schema."""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_login_at", sa.DateTime()),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("tickets",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("give_currency_backend_id", sa.Integer(), nullable=False),
        sa.Column("give_symbol", sa.String(16), nullable=False),
        sa.Column("give_amount", sa.Numeric(36, 12), nullable=False),
        sa.Column("give_coingecko_id", sa.String(64), nullable=False),
        sa.Column("get_currency_backend_id", sa.Integer(), nullable=False),
        sa.Column("get_symbol", sa.String(16), nullable=False),
        sa.Column("get_amount", sa.Numeric(36, 12), nullable=False),
        sa.Column("get_coingecko_id", sa.String(64)),
        sa.Column("get_is_fiat", sa.Boolean(), nullable=False),
        sa.Column("fiat_code", sa.String(8)), sa.Column("rub_kind", sa.String(16)),
        sa.Column("fee_percent", sa.Float(), nullable=False),
        sa.Column("telegram", sa.String(128), nullable=False),
        sa.Column("payout_details", sa.String(512), nullable=False),
        sa.Column("give_usd", sa.Float()), sa.Column("give_rub", sa.Float()), sa.Column("get_usd", sa.Float()),
        sa.Column("raw_payload_json", sa.Text(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("user_id", sa.String(36)), sa.Column("guest_id", sa.String(64)))
    op.create_index("ix_tickets_user_id", "tickets", ["user_id"])
    op.create_index("ix_tickets_guest_id", "tickets", ["guest_id"])
    op.create_index("ix_tickets_user_created", "tickets", ["user_id", "created_at"])
    op.create_table("site_documents", sa.Column("key", sa.String(64), primary_key=True), sa.Column("value", sa.JSON(), nullable=False))
    op.create_table("notifications",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("channel", sa.String(16), nullable=False), sa.Column("text", sa.Text(), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False), sa.Column("next_attempt", sa.DateTime()),
        sa.Column("sent_at", sa.DateTime()), sa.Column("last_error", sa.String(255)), sa.Column("attachment", sa.String(512)))
    op.create_index("ix_notifications_next_attempt", "notifications", ["next_attempt"])


def downgrade():
    for table in ("notifications", "site_documents", "tickets", "users"):
        op.drop_table(table)
