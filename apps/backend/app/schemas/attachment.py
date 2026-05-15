import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


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


class TaskCommentCreate(BaseModel):
    content: str


class TaskCommentResponse(BaseModel):
    id: uuid.UUID
    plan_task_id: uuid.UUID
    user_id: uuid.UUID
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
