from uuid import UUID
from app.dependencies import get_comment_service, get_current_user
from fastapi import APIRouter, Depends, status
from app.models.user import UserORM
from app.schemas.comment import CommentCreate,CommentOut
from app.services.comment_service import CommentService


router = APIRouter(prefix="",tags=["comment"])



@router.post("/tasks/{task_id}/comments",response_model=CommentOut,status_code=status.HTTP_201_CREATED)
async def comment_create(task_id:UUID,data:CommentCreate,service:CommentService = Depends(get_comment_service),user:UserORM = Depends(get_current_user)):
    return await service.create(task_id=task_id,actor_id=user.id,data=data)


@router.get("/tasks/{task_id}/comments",response_model=list[CommentOut],status_code=status.HTTP_200_OK)
async def get_comments(task_id:UUID,service:CommentService = Depends(get_comment_service),user:UserORM = Depends(get_current_user)):
    return await service.list_comments(actor_id=user.id,task_id=task_id)


@router.delete("/comments/{comment_id}",status_code=status.HTTP_204_NO_CONTENT)
async def comment_delete(comment_id:UUID,service:CommentService = Depends(get_comment_service),user:UserORM = Depends(get_current_user)):
    await service.delete_comment(actor_id=user.id,comment_id=comment_id)
    
