# Soft Delete Pattern

Soft delete means a record is never physically removed from the database. Instead, it is marked as inactive. Queries filter out inactive records where needed.

This project uses soft delete on entities that must be preserved for audit, reporting, or referential integrity reasons.

---

## How It Works

Every model in this project inherits from `TimestampMixin`, which adds a `deleted_at` column:

```python
deleted_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
    nullable=True,
)
```

`deleted_at = None` → record is active  
`deleted_at = <timestamp>` → record is soft deleted

For simpler entities where only active/inactive state is needed (no timestamp required), an `is_active` boolean column is used instead:

```python
is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
```

**Rule:** use `is_active` when you only need a flag. Use `deleted_at` when you need to know *when* the record was deactivated.

---

## Deactivating a Record

Set `is_active = False` (or `deleted_at = now()`) in the service layer:

```python
async def deactivate_department(self, db: AsyncSession, department_id: uuid.UUID) -> Department:
    department = await department_repository.get_by_id(db, department_id)
    if not department:
        raise NotFoundError(*messages.DEPARTMENT_NOT_FOUND)

    active_user_count = await user_repository.count_active_by_department(db, department_id)
    if active_user_count > 0:
        raise ValidationError(*messages.DEPARTMENT_HAS_ACTIVE_USERS)

    department.is_active = False
    await db.commit()
    await db.refresh(department)
    return department
```

Business rules (like "cannot deactivate if has active users") live in the service — not the repository, not the endpoint.

---

## Reactivating a Record

```python
async def reactivate_department(self, db: AsyncSession, department_id: uuid.UUID) -> Department:
    department = await department_repository.get_by_id(db, department_id)
    if not department:
        raise NotFoundError(*messages.DEPARTMENT_NOT_FOUND)

    department.is_active = True
    await db.commit()
    await db.refresh(department)
    return department
```

---

## Filtering in Queries

When listing active records only, filter in the repository:

```python
async def get_all_active(self, db: AsyncSession) -> list[Department]:
    result = await db.execute(
        select(Department).where(Department.is_active == True)
    )
    return list(result.scalars().all())
```

For admin views that show all records (active + inactive), omit the filter and include `is_active` in the response schema so the frontend can distinguish them.

---

## Why Not Hard Delete?

| Concern | Why soft delete helps |
|---------|----------------------|
| Audit trail | You can see what existed and when it was deactivated |
| Referential integrity | Foreign keys pointing to the record remain valid |
| Accidental deletion | Reactivation is trivial — no data loss |
| Reporting | Historical data stays queryable |
