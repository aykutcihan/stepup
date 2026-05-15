"""add_return_comment_to_plan_tasks

Revision ID: a1b2c3d4e5f6
Revises: f2a3b4c5d6e7
Create Date: 2026-05-15 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'a1b2c3d4e5f6'
down_revision: str | None = 'f2a3b4c5d6e7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'onboarding_plan_tasks',
        sa.Column('return_comment', sa.Text, nullable=True),
    )


def downgrade() -> None:
    op.drop_column('onboarding_plan_tasks', 'return_comment')
