from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import UUID, String,ForeignKey,DateTime,func
import uuid
from datetime import datetime
from typing import TYPE_CHECKING




if TYPE_CHECKING:
    from app.models.task import TaskORM
    from app.models.user import UserORM
    from app.models.projectmember import ProjectMemberORM


class ProjectORM(Base):
    __tablename__ = "projects"
    
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    description:Mapped[str] = mapped_column(String(255), nullable=True)
    owner_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user: Mapped["UserORM"] = relationship("UserORM", back_populates="projects")
    tasks: Mapped[list["TaskORM"]] = relationship("TaskORM", back_populates="project", cascade="all, delete-orphan")
    members: Mapped[list["ProjectMemberORM"]] = relationship("ProjectMemberORM", back_populates="project", cascade="all, delete-orphan")