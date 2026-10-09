import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    text: str = Field(min_length=7, max_length=255)


class CommentOut(BaseModel):
    id: uuid.UUID
    text: str
    task_id: uuid.UUID
    author_id: uuid.UUID | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
