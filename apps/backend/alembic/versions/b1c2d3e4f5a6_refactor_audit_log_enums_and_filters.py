"""refactor_audit_log_enums_and_filters

Revision ID: b1c2d3e4f5a6
Revises: f2a3b4c5d6e7
Create Date: 2026-05-15 10:00:00.000000

"""
from collections.abc import Sequence

from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = 'b1c2d3e4f5a6'
down_revision: str | None = 'f2a3b4c5d6e7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

audit_action_type_values = [
    "user.invited",
    "user.registered",
    "user.deactivated",
    "user.reactivated",
    "user.updated",
    "plan.created",
    "plan.task_cancelled",
    "task.started",
    "task.completed",
    "task.approved",
    "task.returned",
]

audit_entity_type_values = [
    "user",
    "invitation",
    "plan",
    "task",
]


def upgrade() -> None:
    audit_action_type = postgresql.ENUM(
        *audit_action_type_values,
        name="audit_action_type",
        create_type=False,
    )
    audit_action_type.create(op.get_bind(), checkfirst=True)

    audit_entity_type = postgresql.ENUM(
        *audit_entity_type_values,
        name="audit_entity_type",
        create_type=False,
    )
    audit_entity_type.create(op.get_bind(), checkfirst=True)

    op.execute(
        "ALTER TABLE audit_logs "
        "ALTER COLUMN action TYPE audit_action_type "
        "USING action::audit_action_type"
    )

    op.execute(
        "ALTER TABLE audit_logs "
        "ALTER COLUMN entity_type TYPE audit_entity_type "
        "USING entity_type::audit_entity_type"
    )

    op.create_index('ix_audit_logs_actor_id', 'audit_logs', ['actor_id'], unique=False)
    op.create_index('ix_audit_logs_entity_id', 'audit_logs', ['entity_id'], unique=False)
    op.create_index('ix_audit_logs_entity_type', 'audit_logs', ['entity_type'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_audit_logs_entity_type', table_name='audit_logs')
    op.drop_index('ix_audit_logs_entity_id', table_name='audit_logs')
    op.drop_index('ix_audit_logs_actor_id', table_name='audit_logs')

    op.execute(
        "ALTER TABLE audit_logs "
        "ALTER COLUMN entity_type TYPE VARCHAR(64) "
        "USING entity_type::text"
    )
    op.execute(
        "ALTER TABLE audit_logs "
        "ALTER COLUMN action TYPE VARCHAR(64) "
        "USING action::text"
    )

    op.execute("DROP TYPE IF EXISTS audit_entity_type")
    op.execute("DROP TYPE IF EXISTS audit_action_type")
