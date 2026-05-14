"""add_return_comment_to_onboarding_plan_tasks

Revision ID: a3f1c8e2d047
Revises: 14e90742db5f
Create Date: 2026-05-14 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a3f1c8e2d047'
down_revision: Union[str, None] = '14e90742db5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('onboarding_plan_tasks', sa.Column('return_comment', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('onboarding_plan_tasks', 'return_comment')
