import uuid
from enum import Enum

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ProjectMemberRole(str, Enum):
    OWNER = "owner"
    MEMBER = "member"


class ProjectMemberORM(Base):
    __tablename__ = "project_members"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[ProjectMemberRole] = mapped_column(
        SQLEnum(ProjectMemberRole), nullable=False, default=ProjectMemberRole.MEMBER
    )
    __table_args__ = (UniqueConstraint("project_id", "user_id"),)

    project = relationship("ProjectORM", back_populates="members")
    user = relationship("UserORM", back_populates="project_members")
