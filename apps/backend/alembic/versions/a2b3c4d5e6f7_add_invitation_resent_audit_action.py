"""add invitation_resent audit action

Revision ID: a2b3c4d5e6f7
Revises: f1a2b3c4d5e6
Create Date: 2026-05-16 14:00:00.000000

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'a2b3c4d5e6f7'
down_revision: str | None = 'f1a2b3c4d5e6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TYPE audit_action_type ADD VALUE IF NOT EXISTS 'user.invitation_resent'")


def downgrade() -> None:
    pass
