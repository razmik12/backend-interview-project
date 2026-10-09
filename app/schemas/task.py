import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.task import StatusEnum


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=7, max_length=255)
    assigned_id: uuid.UUID | None = None


class TaskOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    status: StatusEnum
    project_id: uuid.UUID
    assigned_id: uuid.UUID | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskFilter(BaseModel):
    status: StatusEnum | None = None
    assigned_id: uuid.UUID | None = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=255)
    assigned_id: uuid.UUID | None = None

    @field_validator("title")
    @classmethod
    def title_not_null(cls, v):
        if v is None:
            raise ValueError("Title cannot be null")
        return v


class TaskStatusUpdate(BaseModel):
    status: StatusEnum
