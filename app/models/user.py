import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.comment import CommentORM
    from app.models.project import ProjectORM
    from app.models.projectmember import ProjectMemberORM
    from app.models.task import TaskORM


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    tasks: Mapped[list["TaskORM"]] = relationship(
        "TaskORM", back_populates="assigned_user"
    )
    projects: Mapped[list["ProjectORM"]] = relationship(
        "ProjectORM", back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[list["CommentORM"]] = relationship(
        "CommentORM", back_populates="user"
    )
    project_members: Mapped[list["ProjectMemberORM"]] = relationship(
        "ProjectMemberORM", back_populates="user", cascade="all, delete-orphan"
    )
