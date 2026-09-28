from pydantic import BaseModel,Field,ConfigDict
import uuid
from datetime import datetime
from app.models.projectmember import ProjectMemberRole


class ProjectCreate(BaseModel):
    name:str = Field(min_length=1,max_length=255)
    description:str | None = Field(min_length=1,max_length=255,default=None)

class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:uuid.UUID
    name:str
    description:str | None = None
    created_at:datetime
    
class ProjectUpdate(BaseModel):
    name:str | None = Field(min_length=1,max_length=255,default=None)
    description:str | None = Field(min_length=1,max_length=255,default=None)

class MemberAdd(BaseModel):
    user_id:uuid.UUID

class MemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:uuid.UUID
    name:str
    description: str | None = None
    owner_id:uuid.UUID
    role:ProjectMemberRole

class ProjectDetailOut(ProjectOut):
    members:list[MemberOut]


