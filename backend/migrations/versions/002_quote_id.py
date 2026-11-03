"""Make submission of the same signed quote idempotent."""
from alembic import op
import sqlalchemy as sa
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("tickets", sa.Column("quote_id", sa.String(32), nullable=True))
    op.create_unique_constraint("uq_tickets_quote_id", "tickets", ["quote_id"])

def downgrade():
    op.drop_constraint("uq_tickets_quote_id", "tickets", type_="unique")
    op.drop_column("tickets", "quote_id")
