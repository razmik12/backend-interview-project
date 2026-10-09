import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, ForeignKey, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.comment import CommentORM
    from app.models.project import ProjectORM
    from app.models.user import UserORM


class StatusEnum(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    status: Mapped[StatusEnum] = mapped_column(
        SQLEnum(StatusEnum), nullable=False, default=StatusEnum.TODO
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    assigned_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    assigned_user: Mapped["UserORM|None"] = relationship(
        "UserORM", back_populates="tasks"
    )
    project: Mapped["ProjectORM"] = relationship("ProjectORM", back_populates="tasks")
    comments: Mapped[list["CommentORM"]] = relationship(
        "CommentORM", back_populates="task", cascade="all, delete-orphan"
    )
