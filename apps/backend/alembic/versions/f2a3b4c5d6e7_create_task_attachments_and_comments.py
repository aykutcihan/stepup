"""create_task_attachments_and_comments

Revision ID: f2a3b4c5d6e7
Revises: e1b2c3d4e5f6
Create Date: 2026-05-14 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = 'f2a3b4c5d6e7'
down_revision: Union[str, None] = 'e1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'task_attachments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('plan_task_id', UUID(as_uuid=True), sa.ForeignKey('onboarding_plan_tasks.id'), nullable=False),
        sa.Column('uploaded_by', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('object_name', sa.String(512), nullable=False),
        sa.Column('file_type', sa.String(128), nullable=False),
        sa.Column('file_size', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_task_attachments_plan_task_id', 'task_attachments', ['plan_task_id'])

    op.create_table(
        'task_comments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('plan_task_id', UUID(as_uuid=True), sa.ForeignKey('onboarding_plan_tasks.id'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_task_comments_plan_task_id', 'task_comments', ['plan_task_id'])


def downgrade() -> None:
    op.drop_index('ix_task_comments_plan_task_id', 'task_comments')
    op.drop_table('task_comments')
    op.drop_index('ix_task_attachments_plan_task_id', 'task_attachments')
    op.drop_table('task_attachments')
