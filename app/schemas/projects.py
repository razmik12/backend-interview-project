from pydantic import BaseModel,Field,ConfigDict
import uuid
from datetime import datetime


class ProjectCreate(BaseModel):
    name:str = Field(min_length=1,max_length=255)
    description:str | None = Field(default=None,max_length=255)
    

class ProjectOut(BaseModel):
    id:uuid.UUID
    name:str = Field(min_length=1,max_length=255)
    description:str | None = Field(default=None,max_length=255)
    owner_id:uuid.UUID
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)