"""add_overdue_task_status

Revision ID: e1b2c3d4e5f6
Revises: c9a4b2e1f8d3
Create Date: 2026-05-14 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'e1b2c3d4e5f6'
down_revision: Union[str, None] = 'c9a4b2e1f8d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE onboarding_plan_task_status ADD VALUE IF NOT EXISTS 'overdue'")


def downgrade() -> None:
    pass
