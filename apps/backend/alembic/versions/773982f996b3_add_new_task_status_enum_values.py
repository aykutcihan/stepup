"""add_new_task_status_enum_values

Revision ID: 773982f996b3
Revises: 1a0611e7e039
Create Date: 2026-05-14 02:33:00.859206

"""
from collections.abc import Sequence

from alembic import op

revision: str = '773982f996b3'
down_revision: str | None = '1a0611e7e039'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TYPE onboarding_plan_task_status ADD VALUE IF NOT EXISTS 'in_progress'")
    op.execute("ALTER TYPE onboarding_plan_task_status ADD VALUE IF NOT EXISTS 'completed'")
    op.execute("ALTER TYPE onboarding_plan_task_status ADD VALUE IF NOT EXISTS 'approved'")
    op.execute("ALTER TYPE onboarding_plan_task_status ADD VALUE IF NOT EXISTS 'returned'")


def downgrade() -> None:
    pass