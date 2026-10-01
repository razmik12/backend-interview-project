from uuid import UUID
from app.dependencies import get_project_services, get_current_user
from fastapi import APIRouter, Depends, status
from app.models.user import UserORM
from app.schemas.projects import MemberAdd, MemberOut, ProjectCreate,ProjectOut,ProjectDetailOut, ProjectUpdate
from app.services.project_service import ProjectService




router = APIRouter(prefix="/project",tags=["project"])



@router.post("/create",response_model=ProjectOut,status_code=status.HTTP_201_CREATED)
async def create_project(data:ProjectCreate,service:ProjectService = Depends(get_project_services),user:UserORM = Depends(get_current_user)):
    return await service.create_project(data=data,owner_id=user.id)


@router.get("/project",response_model=list[ProjectOut],status_code=status.HTTP_200_OK)
async def get_my_projects(service:ProjectService = Depends(get_project_services),user:UserORM = Depends(get_current_user)):
    return await service.list_my_projects(user_id=user.id)



@router.get("/{project_id}",response_model=ProjectDetailOut,status_code=status.HTTP_200_OK)
async def get_all_projects(project_id:UUID,service:ProjectService = Depends(get_project_services),user:UserORM = Depends(get_current_user)):
    return await service.get_project_detail(project_id=project_id,user_id=user.id)


@router.patch("/update/{project_id}",response_model=ProjectOut,status_code=status.HTTP_202_ACCEPTED)
async def update_project(data:ProjectUpdate,project_id:UUID,service:ProjectService = Depends(get_project_services),user:UserORM = Depends(get_current_user)):
    return await service.update_project(project_id=project_id,user_id=user.id,data=data)



@router.delete("/update/{project_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id:UUID,service:ProjectService = Depends(get_project_services),user:UserORM = Depends(get_current_user)):
    return await service.delete_project(project_id=project_id,user_id=user.id)


@router.post("/{project_id}/members",response_model=MemberOut,status_code=status.HTTP_201_CREATED)
async def member_add(project_id:UUID,data:MemberAdd,service:ProjectService = Depends(get_project_services),user:UserORM = Depends(get_current_user)):
    return await service.add_member(project_id=project_id,data=data,owner_id=user.id)
