from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import UUID, String,ForeignKey,DateTime,func, Enum as SQLEnum
import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.user import UserORM
    from app.models.project import ProjectORM
    from app.models.comment import CommentORM

class StatusEnum(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskORM(Base):
    __tablename__ = "tasks"
    
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title:Mapped[str] = mapped_column(String(200), nullable=False)
    description:Mapped[str] = mapped_column(String(255), nullable=True)
    status:Mapped[StatusEnum] = mapped_column(SQLEnum(StatusEnum), nullable=False, default=StatusEnum.TODO)
    project_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("projects.id",ondelete="CASCADE"), nullable=False)
    assigned_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="SET NULL"), nullable=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    assigned_user: Mapped["UserORM"] = relationship("UserORM", back_populates="tasks")
    project: Mapped["ProjectORM"] = relationship("ProjectORM", back_populates="tasks")
    comments: Mapped[list["CommentORM"]] = relationship("CommentORM", back_populates="task", cascade="all, delete-orphan")