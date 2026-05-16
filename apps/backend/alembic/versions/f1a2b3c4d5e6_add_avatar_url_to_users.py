"""add avatar_url to users

Revision ID: f1a2b3c4d5e6
Revises: c0d1e2f3a4b5
Create Date: 2026-05-16 12:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'f1a2b3c4d5e6'
down_revision: str = 'c0d1e2f3a4b5'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('users', sa.Column('avatar_url', sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'avatar_url')
