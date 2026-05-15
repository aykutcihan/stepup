import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class TaskAttachmentResponse(BaseModel):
    id: uuid.UUID
    plan_task_id: uuid.UUID
    uploaded_by: uuid.UUID
    file_name: str
    file_type: str
    file_size: int
    download_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='before')
    @classmethod
    def compute_download_url(cls, v):
        if isinstance(v, dict):
            return v
        from app.services.storage_service import StorageService
        storage = StorageService()
        return {
            'id': v.id,
            'plan_task_id': v.plan_task_id,
            'uploaded_by': v.uploaded_by,
            'file_name': v.file_name,
            'file_type': v.file_type,
            'file_size': v.file_size,
            'download_url': storage.signed_url(v.object_name),
            'created_at': v.created_at,
        }


class TaskCommentCreate(BaseModel):
    content: str


class TaskCommentResponse(BaseModel):
    id: uuid.UUID
    plan_task_id: uuid.UUID
    user_id: uuid.UUID
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
