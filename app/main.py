from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
import logging

from app.config import settings
from app.exceptions.app_exception import AppError
from app.exceptions.handlers import app_exception_handler
from app.middleware.logging import LoggingMiddleware
from app.routers.auth import router as auth_router
from app.routers.comment import router as comment_router
from app.routers.project import router as project_router
from app.routers.task import router as task_router

logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.warning("Starting up...")
    redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    app.state.redis = redis_client

    yield

    await redis_client.aclose()
    logger.warning("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=auth_router)
app.include_router(router=project_router)
app.include_router(router=comment_router)
app.include_router(router=task_router)


app.add_exception_handler(AppError, app_exception_handler)
