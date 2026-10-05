from uuid import UUID
from app.dependencies import get_task_service, get_current_user
from fastapi import APIRouter, Depends, status
from app.models.user import UserORM
from app.schemas.task import TaskCreate, TaskOut, TaskFilter,TaskStatusUpdate,TaskUpdate
from app.services.task_service import TaskService



router = APIRouter(prefix="/projects",tags=["task"])



@router.post("/{project_id}/tasks",response_model=TaskOut,status_code=status.HTTP_201_CREATED)
async def task_create(data:TaskCreate,project_id:UUID,service:TaskService = Depends(get_task_service),user:UserORM = Depends(get_current_user)):
    return await service.create_task(data=data,project_id=project_id,actor_id=user.id)

@router.get("/{project_id}/tasks",response_model=list[TaskOut],status_code=status.HTTP_200_OK)
async def get_tasks(project_id:UUID,service:TaskService = Depends(get_task_service),user:UserORM = Depends(get_current_user),data_filtr:TaskFilter = Depends()):
    return await service.list_tasks(project_id=project_id,actor_id=user.id,filters=data_filtr)

@router.patch("/{project_id}/tasks/{task_id}/status",response_model=TaskOut,status_code=status.HTTP_202_ACCEPTED)
async def update_task_status(data:TaskStatusUpdate,project_id:UUID,task_id:UUID,service:TaskService = Depends(get_task_service),user:UserORM = Depends(get_current_user)):
    return await service.update_status(data=data,actor_id=user.id,task_id=task_id,project_id=project_id)


@router.patch("/{project_id}/tasks/{task_id}",response_model=TaskOut,status_code=status.HTTP_202_ACCEPTED)
async def task_update(data:TaskUpdate,project_id:UUID,task_id:UUID,service:TaskService = Depends(get_task_service),user:UserORM = Depends(get_current_user)):
    return await service.update_task(data=data,project_id=project_id,actor_id=user.id,task_id=task_id)

@router.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
async def task_delete(task_id:UUID,service:TaskService = Depends(get_task_service),user:UserORM = Depends(get_current_user)):
     await service.delete_task(task_id=task_id,owner_id=user.id)
     