"""merge heads

Revision ID: c0d1e2f3a4b5
Revises: a3f1c8e2d047, a1b2c3d4e5f6, b1c2d3e4f5a6
Create Date: 2026-05-15 14:00:00.000000

"""
from collections.abc import Sequence

revision: str = 'c0d1e2f3a4b5'
down_revision: tuple[str, ...] = ('a3f1c8e2d047', 'a1b2c3d4e5f6', 'b1c2d3e4f5a6')
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
