import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.services.department_service import DepartmentService

router = APIRouter()
department_service = DepartmentService()


@router.get("/", response_model=list[DepartmentResponse])
async def get_departments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> list[DepartmentResponse]:
    departments = await department_service.get_all_departments(db=db)
    return [DepartmentResponse.model_validate(d) for d in departments]


@router.patch("/{department_id}/reactivate", response_model=DepartmentResponse)
async def reactivate_department(
    department_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> DepartmentResponse:
    department = await department_service.reactivate_department(db=db, department_id=department_id)
    return DepartmentResponse.model_validate(department)


@router.patch("/{department_id}/deactivate", response_model=DepartmentResponse)
async def deactivate_department(
    department_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> DepartmentResponse:
    department = await department_service.deactivate_department(db=db, department_id=department_id)
    return DepartmentResponse.model_validate(department)


@router.patch("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: uuid.UUID,
    data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> DepartmentResponse:
    department = await department_service.update_department(db=db, department_id=department_id, data=data)
    return DepartmentResponse.model_validate(department)


@router.post("/", response_model=DepartmentResponse, status_code=201)
async def create_department(
    data: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> DepartmentResponse:
    department = await department_service.create_department(db=db, data=data)
    return DepartmentResponse.model_validate(department)
