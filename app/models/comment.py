from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import UUID, String,ForeignKey,DateTime,func, Enum as SQLEnum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.user import UserORM
    from app.models.task import TaskORM



class CommentORM(Base):
    __tablename__ = "comments"
    
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text:Mapped[str] = mapped_column(String(255), nullable=False)
    task_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("tasks.id",ondelete="CASCADE"), nullable=False)
    author_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="SET NULL"), nullable=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user: Mapped["UserORM"] = relationship("UserORM", back_populates="comments")
    task: Mapped["TaskORM"] = relationship("TaskORM", back_populates="comments")