"""add_audit_log_table

Revision ID: c9a4b2e1f8d3
Revises: a3f1c8e2d047
Create Date: 2026-05-14 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = 'c9a4b2e1f8d3'
down_revision: Union[str, None] = 'a3f1c8e2d047'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'audit_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('actor_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('action', sa.String(64), nullable=False, index=True),
        sa.Column('entity_type', sa.String(64), nullable=False),
        sa.Column('entity_id', UUID(as_uuid=True), nullable=False),
        sa.Column('detail', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('ix_audit_logs_created_at', 'audit_logs', ['created_at'])


def downgrade() -> None:
    op.drop_index('ix_audit_logs_created_at', 'audit_logs')
    op.drop_index('ix_audit_logs_action', 'audit_logs')
    op.drop_table('audit_logs')
