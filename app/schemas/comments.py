from pydantic import BaseModel,Field,ConfigDict
import uuid
from datetime import datetime



class CommentCreate(BaseModel):
    text:str = Field(min_length=1,max_length=255)


class CommentOut(BaseModel):
    id:uuid.UUID
    text:str
    author_id:uuid.UUID | None = None
    task_id:uuid.UUID
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)