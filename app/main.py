from fastapi import FastAPI
from app.exceptions.app_exception import AppError
from app.routers.auth import router as auth_router
from app.exceptions.handlers import app_exception_handler
app=FastAPI()


app.include_router(router=auth_router)

app.add_exception_handler(AppError,app_exception_handler)