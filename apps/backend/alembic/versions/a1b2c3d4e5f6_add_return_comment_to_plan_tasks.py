"""add_return_comment_to_plan_tasks

Revision ID: a1b2c3d4e5f6
Revises: f2a3b4c5d6e7
Create Date: 2026-05-15 00:00:00.000000

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'a1b2c3d4e5f6'
down_revision: str | None = 'f2a3b4c5d6e7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE onboarding_plan_tasks ADD COLUMN IF NOT EXISTS return_comment TEXT"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE onboarding_plan_tasks DROP COLUMN IF EXISTS return_comment"
    )
