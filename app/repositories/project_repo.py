from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import ProjectORM
from app.models.projectmember import ProjectMemberORM


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_project(
        self, name: str, owner_id: UUID, description: str | None = None
    ) -> ProjectORM:
        project = ProjectORM(name=name, description=description, owner_id=owner_id)
        self.session.add(project)
        await self.session.flush()
        return project

    async def get_by_id(self, project_id: UUID) -> ProjectORM | None:
        return await self.session.get(ProjectORM, project_id)

    async def get_projects(self, user_id: UUID) -> list[ProjectORM]:
        result = await self.session.execute(
            select(ProjectORM)
            .join(ProjectMemberORM,ProjectORM.members)
            .where(ProjectMemberORM.user_id == user_id)

        )
        return list(result.scalars().all())

    async def get_with_members(self, project_id: UUID) -> ProjectORM | None:
        result = await self.session.execute(
            select(ProjectORM)
            .where(ProjectORM.id == project_id)
            .options(selectinload(ProjectORM.members))
        )
        return result.scalar_one_or_none()

    async def update_project(self, project: ProjectORM, data: dict) -> ProjectORM:
        for key, value in data.items():
            setattr(project, key, value)
        return project

    async def delete_project(self, project: ProjectORM) -> None:
        await self.session.delete(project)
