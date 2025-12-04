"""Add closed_at column to tasks table.

This represents the Phase 2 change:
    - Task gains a 'closed_at' column to record when it was auto-closed.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_add_closed_at_to_tasks"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply the migration: add closed_at column."""
    op.add_column("tasks", sa.Column("closed_at", sa.Date(), nullable=True))


def downgrade() -> None:
    """Rollback the migration: drop closed_at column."""
    op.drop_column("tasks", "closed_at")


