"""Seed script: inserts 20 varied audit log entries for demo purposes."""
import asyncio
import os
import uuid
from datetime import UTC, datetime, timedelta
import random

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.audit_log import AuditLog
from app.enums.audit_enums import AuditActionType, AuditEntityType

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

HR_ADMIN_ID    = uuid.UUID("00000000-0000-0000-0000-000000000001")
MANAGER_ID     = uuid.UUID("00000000-0000-0000-0000-000000000002")
EMPLOYEE_ID    = uuid.UUID("00000000-0000-0000-0000-000000000003")
DEPT_ID        = uuid.UUID("00000000-0000-0000-0000-000000000102")

ENTRIES = [
    (HR_ADMIN_ID,  AuditActionType.user_invited,         AuditEntityType.user,       EMPLOYEE_ID,  -30),
    (HR_ADMIN_ID,  AuditActionType.user_invited,         AuditEntityType.user,       MANAGER_ID,   -28),
    (HR_ADMIN_ID,  AuditActionType.user_registered,      AuditEntityType.user,       EMPLOYEE_ID,  -27),
    (HR_ADMIN_ID,  AuditActionType.user_registered,      AuditEntityType.user,       MANAGER_ID,   -26),
    (HR_ADMIN_ID,  AuditActionType.user_updated,         AuditEntityType.user,       EMPLOYEE_ID,  -25),
    (HR_ADMIN_ID,  AuditActionType.plan_created,         AuditEntityType.plan,       uuid.uuid4(), -24),
    (MANAGER_ID,   AuditActionType.task_started,         AuditEntityType.task,       uuid.uuid4(), -22),
    (EMPLOYEE_ID,  AuditActionType.task_completed,       AuditEntityType.task,       uuid.uuid4(), -20),
    (MANAGER_ID,   AuditActionType.task_approved,        AuditEntityType.task,       uuid.uuid4(), -18),
    (HR_ADMIN_ID,  AuditActionType.user_invited,         AuditEntityType.user,       uuid.uuid4(), -16),
    (HR_ADMIN_ID,  AuditActionType.user_invitation_resent, AuditEntityType.invitation, uuid.uuid4(), -15),
    (EMPLOYEE_ID,  AuditActionType.task_completed,       AuditEntityType.task,       uuid.uuid4(), -14),
    (MANAGER_ID,   AuditActionType.task_returned,        AuditEntityType.task,       uuid.uuid4(), -12),
    (EMPLOYEE_ID,  AuditActionType.task_completed,       AuditEntityType.task,       uuid.uuid4(), -10),
    (MANAGER_ID,   AuditActionType.task_approved,        AuditEntityType.task,       uuid.uuid4(),  -9),
    (HR_ADMIN_ID,  AuditActionType.user_deactivated,     AuditEntityType.user,       uuid.uuid4(),  -7),
    (HR_ADMIN_ID,  AuditActionType.user_reactivated,     AuditEntityType.user,       uuid.uuid4(),  -5),
    (HR_ADMIN_ID,  AuditActionType.plan_created,         AuditEntityType.plan,       uuid.uuid4(),  -4),
    (MANAGER_ID,   AuditActionType.plan_task_cancelled,  AuditEntityType.task,       uuid.uuid4(),  -2),
    (HR_ADMIN_ID,  AuditActionType.user_updated,         AuditEntityType.user,       MANAGER_ID,    -1),
]

async def seed():
    async with AsyncSessionLocal() as db:
        now = datetime.now(UTC)
        for actor_id, action, entity_type, entity_id, days_ago in ENTRIES:
            log = AuditLog(
                id=uuid.uuid4(),
                actor_id=actor_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                created_at=now + timedelta(days=days_ago, hours=random.randint(0, 8)),
            )
            db.add(log)
        await db.commit()
        print(f"Inserted {len(ENTRIES)} audit log entries.")

if __name__ == "__main__":
    asyncio.run(seed())
