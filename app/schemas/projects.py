import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.projectmember import ProjectMemberRole


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ProjectOut(BaseModel):
    id: uuid.UUID
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    owner_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MemberOut(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    user_id: uuid.UUID
    role: ProjectMemberRole
    model_config = ConfigDict(from_attributes=True)


class ProjectDetailOut(ProjectOut):
    members: list[MemberOut]


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

    @field_validator("name")
    @classmethod
    def name_not_null(cls, v: str | None) -> str:
        if v is None:
            raise ValueError("name cannot be null")
        return v


class MemberAdd(BaseModel):
    user_id: uuid.UUID
