from fastapi import FastAPI
from app.exceptions.app_exception import AppError
from app.routers.auth import router as auth_router
from app.routers.project import router as project_router
from app.routers.comment import router as comment_router
from app.routers.task import router as task_router
from app.exceptions.handlers import app_exception_handler

app=FastAPI()


app.include_router(router=auth_router)
app.include_router(router=project_router)
app.include_router(router=comment_router)
app.include_router(router=task_router)
app.add_exception_handler(AppError,app_exception_handler)