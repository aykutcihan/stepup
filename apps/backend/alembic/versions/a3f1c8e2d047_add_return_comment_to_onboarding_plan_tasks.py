"""add_return_comment_to_onboarding_plan_tasks

Revision ID: a3f1c8e2d047
Revises: 14e90742db5f
Create Date: 2026-05-14 10:00:00.000000

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'a3f1c8e2d047'
down_revision: str | None = '14e90742db5f'
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
